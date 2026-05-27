"""
ExportMongoDB.py
-------------------
Reads poverty-related indicators from a MySQL database using stored
procedures and inserts them into a MongoDB database, mirroring the
four-collection structure:
    - period
    - education_indicator
    - economy_indicator
    - employment_indicator

Dependencies: pymongo, mysql-connector-python
Configuration: config.txt (see config.example.txt)
"""

import os
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from mysql.connector import connect, Error
from decimal import Decimal


def cargar_config(ruta='config.txt'):
    """
    Reads connection settings from a plain-text config file.

    Each line must follow the format: key=value
    Blank lines and lines without '=' are ignored.

    Args:
        ruta (str): Path to the config file. Defaults to 'config.txt'.

    Returns:
        dict: Configuration key-value pairs.
    """
    config = {}
    with open(ruta, 'r') as f:
        for linea in f:
            linea = linea.strip()
            if linea and '=' in linea:
                # Split on the first '=' only, in case the value contains '='
                clave, valor = linea.split('=', 1)
                config[clave.strip()] = valor.strip()
    return config

# Resolve config path relative to this script's directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
config = cargar_config(os.path.join(BASE_DIR, '..', 'config.txt'))


def conectar_mysql():
    """
    Establishes a connection to the MySQL database.

    Returns:
        mysql.connector.connection.MySQLConnection | None:
            An open connection on success, or None on failure.
    """
    try:
        conexion = connect(
            host=config['host'],
            user=config['user'],
            password=config['password'],
            database=config['database']
        )
        print(f"MySQL connection established: {config['host']}")
        return conexion
    except Error as e:
        print(f"MySQL connection error: {e}")
        return None


def conectar_mongo():
    """
    Establishes a connection to MongoDB and returns the target database.

    Returns:
        pymongo.database.Database | None:
            The target database on success, or None on failure.
    """
    try:
        cliente = MongoClient(
            host=config['mongo_host'],
            port=int(config['mongo_port']),
            username=config.get('mongo_user') or None,
            password=config.get('mongo_password') or None
        )
        # Verify the connection is reachable
        cliente.admin.command('ping')
        db = cliente[config['mongo_database']]
        print(f"MongoDB connection established: {config['mongo_host']}:{config['mongo_port']}")
        return db
    except PyMongoError as e:
        print(f"MongoDB connection error: {e}")
        return None


def llamar_sp(cursor, nombre_sp):
    """
    Calls a stored procedure and returns its result set as a
    list of dictionaries.

    Args:
        cursor: Active MySQL cursor.
        nombre_sp (str): Name of the stored procedure to call.

    Returns:
        list[dict]: List of rows as dictionaries, keyed by column name.
    """
    def convertir(valor):
        # MySQL returns DECIMAL columns as decimal.Decimal, which MongoDB cannot serialize
        if isinstance(valor, Decimal):
            return float(valor)
        return valor

    cursor.callproc(nombre_sp)
    for resultado in cursor.stored_results():
        columnas = [col[0] for col in resultado.description]
        return [{col: convertir(val) for col, val in zip(columnas, fila)} for fila in resultado.fetchall()]
    return []


def exportar(mysql_con, db):
    """
    Reads data from MySQL via stored procedures and inserts it into
    MongoDB across four collections.

    Stored procedures called:
        - sp_get_all_periods    → period
        - sp_get_all_education  → education_indicator
        - sp_get_all_economy    → economy_indicator
        - sp_get_all_employment → employment_indicator

    Each collection is cleared before insertion to avoid duplicates
    on re-runs.

    Args:
        mysql_con: Open MySQL connection.
        db (pymongo.database.Database): Target MongoDB database.
    """
    cursor = mysql_con.cursor()

    colecciones = ['period', 'education_indicator', 'economy_indicator', 'employment_indicator']
    procedimientos = ['sp_get_all_periods', 'sp_get_all_education', 'sp_get_all_economy', 'sp_get_all_employment']

    for coleccion, sp in zip(colecciones, procedimientos):
        print(f"\nExporting '{coleccion}' via {sp}...")

        registros = llamar_sp(cursor, sp)
        if not registros:
            print(f"  No data returned by {sp}, skipping.")
            continue

        # Clear the collection before inserting to avoid duplicates on re-runs
        db[coleccion].delete_many({})
        db[coleccion].insert_many(registros)
        print(f"  [OK] {len(registros)} documents inserted into '{coleccion}'.")

    cursor.close()


if __name__ == '__main__':
    mysql_con = conectar_mysql()
    db = conectar_mongo()

    if mysql_con is not None and db is not None:
        exportar(mysql_con, db)
        mysql_con.close()
        print("\nExport complete.")
    else:
        print("Aborting: could not establish one or both connections.")