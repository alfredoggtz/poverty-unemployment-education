"""
migrateDatabases.py
-------------------
Migrates data from the MySQL 'pobreza' database to MongoDB.

Reads connection credentials from config.txt and uses the project's
stored procedures to extract data, mirroring the four-collection structure:
    - period
    - education_indicator
    - economy_indicator
    - employment_indicator

Dependencies: pymysql, pymongo
Configuration: config.txt (one level above this script)
"""

import os
import sys
import pymysql
from pymongo import MongoClient
from decimal import Decimal


def load_config(path='config.txt'):
    config = {}
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and '=' in line:
                key, value = line.split('=', 1)
                config[key.strip()] = value.strip()
    return config


BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, '..', 'config.txt')
config      = load_config(CONFIG_PATH)

MYSQL_DB_NAME = config['database']
MONGO_DB_NAME = config['mongo_database']

COLLECTIONS = {
    'period': 'sp_get_all_periods',
    'education_indicator': 'sp_get_all_education',
    'economy_indicator': 'sp_get_all_economy',
    'employment_indicator': 'sp_get_all_employment',
}


def convert(value):
    """Converts types not serializable by MongoDB (Decimal -> float)."""
    if isinstance(value, Decimal):
        return float(value)
    return value


def migrate_collection(collection_name, sp_name):
    """Calls the stored procedure and inserts all returned documents into MongoDB."""
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


# MySQL connection
print("Connecting to MySQL...")
try:
    mysql_conn = pymysql.connect(
        host=config['host'],
        user=config['user'],
        password=config['password']
    )
except Exception as e:
    print(f"[ERROR] MySQL connection error: {e}")
    sys.exit(1)

with mysql_conn.cursor() as cursor:
    cursor.execute("SHOW DATABASES")
    available_dbs = [row[0] for row in cursor.fetchall()]
    if MYSQL_DB_NAME not in available_dbs:
        print(f"[ERROR] MySQL database '{MYSQL_DB_NAME}' does not exist.")
        mysql_conn.close()
        sys.exit(1)

mysql_conn.select_db(MYSQL_DB_NAME)
print(f"[OK] Connected to MySQL database '{MYSQL_DB_NAME}'.")

# MongoDB connection
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

# Migration
print(f"\nStarting migration: MySQL '{MYSQL_DB_NAME}' -> MongoDB '{MONGO_DB_NAME}'")
print(f"Collections: {list(COLLECTIONS.keys())}\n")

for collection, sp in COLLECTIONS.items():
    migrate_collection(collection, sp)

# Cleanup
mysql_conn.close()
mongo_client.close()
print("\n[OK] Migration complete. Connections closed.")