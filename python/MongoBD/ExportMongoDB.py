"""
ExportMongoDB.py
-------------------
Migrates data from the MySQL 'pobreza' database to MongoDB.

Reads connection credentials from config.txt and uses the project's
stored procedures to extract data, mirroring the four-collection structure:
    - period
    - education_indicator
    - economy_indicator
    - employment_indicator

Workflow:
    1. Parse config.txt to obtain MySQL and MongoDB credentials.
    2. Connect to MySQL directly with the target database.
    3. Connect to MongoDB, drop the existing database, and recreate it fresh.
    4. For each collection, call the corresponding stored procedure, convert
       any non-serialisable types, and bulk-insert the rows into MongoDB.
    5. Close both connections.

Dependencies: pymysql, pymongo
Configuration: config.txt (one level above this script)
"""

import os
import sys
import pymysql
from pymongo import MongoClient
from decimal import Decimal


# ── Config ─────────────────────────────────────────────────────────────────────

def load_config(path: str = 'config.txt') -> dict:
    """
    Parse a key=value configuration file into a dictionary.

    Lines that are blank or do not contain an ``=`` sign are silently ignored.
    The first ``=`` on a line is used as the delimiter, so values may themselves
    contain ``=`` characters without being truncated.

    Args:
        path (str): Path to the configuration file. Defaults to ``'config.txt'``
                    in the current working directory.

    Returns:
        dict: Mapping of setting names to their string values.

    Raises:
        FileNotFoundError: If ``path`` does not point to an existing file.
        IOError: If the file cannot be opened for reading.
    """
    config = {}
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and '=' in line:
                key, value = line.split('=', 1)
                config[key.strip()] = value.strip()
    return config


# Resolve the config file path relative to this script so the migration works
# regardless of the current working directory when it is invoked.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, '..', 'config.txt')
config = load_config(CONFIG_PATH)

MYSQL_DB_NAME = config['database']
MONGO_DB_NAME = config['mongo_database']

# Maps each MongoDB collection name to the MySQL stored procedure that supplies
# its data. The procedure is expected to return a single result set of rows.
COLLECTIONS = {
    'period': 'sp_get_all_periods',
    'education_indicator': 'sp_get_all_education',
    'economy_indicator': 'sp_get_all_economy',
    'employment_indicator': 'sp_get_all_employment',
}


# ── Helpers ────────────────────────────────────────────────────────────────────

def convert(value):
    """
    Convert a value to a MongoDB-compatible Python type.

    The MySQL driver may return ``Decimal`` objects for numeric columns.
    MongoDB's BSON encoder does not support ``Decimal``, so they must be
    converted to ``float`` before insertion.

    Args:
        value: Any value returned from a MySQL query row.

    Returns:
        float | any: A ``float`` if ``value`` is a ``Decimal``; otherwise the
                     original value is returned unchanged.
    """
    if isinstance(value, Decimal):
        return float(value)
    return value


def migrate_collection(collection_name: str, sp_name: str) -> None:
    """
    Extract all rows from a MySQL stored procedure and insert them into MongoDB.

    Uses the module-level ``mysql_conn`` and ``mongo_db`` objects, which must
    already be open and authenticated before this function is called.

    Args:
        collection_name (str): Name of the MongoDB collection to insert into.
        sp_name (str):         Name of the MySQL stored procedure to call.
    """
    print(f"\nMigrating '{collection_name}' via {sp_name}...")
    try:
        with mysql_conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.callproc(sp_name)

            rows = []
            while True:
                result = cursor.fetchall()
                if result:
                    rows.extend(result)
                if not cursor.nextset():
                    break

            if not rows:
                print(f"  [SKIP] No data returned by {sp_name}.")
                return

            rows = [{k: convert(v) for k, v in row.items()} for row in rows]
            mongo_db[collection_name].insert_many(rows)
            print(f"  [OK] {len(rows)} documents inserted into '{collection_name}'.")

    except Exception as e:
        print(f"  [ERROR] Error migrating '{collection_name}': {e}")


# ── MySQL connection ────────────────────────────────────────────────────────────

print("Connecting to MySQL...")
try:
    mysql_conn = pymysql.connect(
        host=config['host'],
        user=config['user'],
        password=config['password'],
        database=MYSQL_DB_NAME
    )
    print(f"[OK] Connected to MySQL database '{MYSQL_DB_NAME}'.")
except pymysql.err.OperationalError as e:
    if e.args[0] == 1049:
        print(f"[ERROR] MySQL database '{MYSQL_DB_NAME}' does not exist.")
    else:
        print(f"[ERROR] MySQL connection error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"[ERROR] MySQL connection error: {e}")
    sys.exit(1)


# ── MongoDB connection ─────────────────────────────────────────────────────────

print("Connecting to MongoDB...")
try:
    mongo_client = MongoClient(
        host=config['mongo_host'],
        port=int(config['mongo_port']),
        username=config.get('mongo_user') or None,
        password=config.get('mongo_password') or None
    )
    mongo_client.admin.command('ping')
except Exception as e:
    print(f"[ERROR] MongoDB connection error: {e}")
    mysql_conn.close()
    sys.exit(1)

mongo_client.drop_database(MONGO_DB_NAME)
print(f"[DROP] MongoDB database '{MONGO_DB_NAME}' dropped.")

mongo_db = mongo_client[MONGO_DB_NAME]
print(f"[OK] MongoDB database '{MONGO_DB_NAME}' ready.")


# ── Migration ──────────────────────────────────────────────────────────────────

print(f"\nStarting migration: MySQL '{MYSQL_DB_NAME}' -> MongoDB '{MONGO_DB_NAME}'")
print(f"Collections: {list(COLLECTIONS.keys())}\n")

for collection, sp in COLLECTIONS.items():
    migrate_collection(collection, sp)


# ── Cleanup ────────────────────────────────────────────────────────────────────

mysql_conn.close()
mongo_client.close()
print("\n[OK] Migration complete. Connections closed.")