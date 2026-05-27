"""
InsertMySQL.py
-----------------
Loads poverty-related indicators from a CSV file and inserts them into
a MySQL database using stored procedures. If the target database does
not exist, it is automatically recreated from a SQL backup file.

Dependencies: pandas, mysql-connector-python
Configuration: config.txt (one level above this script's directory)
"""

import os
import shutil
import subprocess
import pandas as pd
from mysql.connector import connect, Error


def load_config(path):
    """Reads database connection settings from a plain-text config file.

    Parses each non-empty line with the format ``key=value``.
    Splits only on the first ``=`` to support values that contain ``=``.

    Args:
        path (str): Absolute path to the config file.

    Returns:
        dict[str, str]: Configuration key-value pairs.
    """
    config = {}
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and '=' in line:
                key, value = line.split('=', 1)
                config[key.strip()] = value.strip()
    return config


def find_mysql():
    """Detects the mysql CLI executable automatically.

    Search order:
        1. System PATH (works if MySQL is properly installed).
        2. Common Windows installation directories.

    Returns:
        str: Full path to mysql.exe, or None if not found.
    """
    path = shutil.which('mysql')
    if path:
        return path

    common_paths = [
        r"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe",
        r"C:\Program Files\MySQL\MySQL Server 8.4\bin\mysql.exe",
        r"C:\Program Files\MySQL\MySQL Server 5.7\bin\mysql.exe",
        r"C:\Program Files (x86)\MySQL\MySQL Server 8.0\bin\mysql.exe",
        r"C:\xampp\mysql\bin\mysql.exe",
        r"C:\wamp64\bin\mysql\mysql8.0\bin\mysql.exe",
    ]
    for p in common_paths:
        if os.path.exists(p):
            return p
    return None


def run_backup():
    """Executes DataBaseBackup.sql via the mysql CLI to recreate the database.

    Detects the mysql executable automatically using ``find_mysql()``.
    Reads the backup file from the same directory as this script.

    Returns:
        bool: True if the backup ran successfully, False otherwise.
    """
    mysql_path = find_mysql()
    if not mysql_path:
        print("[ERROR] mysql.exe not found. Install MySQL and add it to PATH.")
        return False
    print(f"Using mysql at: {mysql_path}")
    subprocess.run(
        [mysql_path, f"-u{db_config['user']}", f"-p{db_config['password']}"],
        input=open(BACKUP_PATH).read(),
        text=True
    )
    print("Database created successfully.")
    return True


def open_connection():
    """Opens and returns a global MySQL connection, recreating the DB if needed.

    Attempts to connect directly to the target database. If the database
    does not exist (error 1049), runs the SQL backup to recreate it and
    retries the connection. If the database exists, it is also replaced
    from backup to ensure a clean state before insertion.

    Returns:
        mysql.connector.connection.MySQLConnection | None:
            An open connection on success, or None on failure.
    """
    try:
        conn = connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=DB_NAME
        )
        print(f"Database '{DB_NAME}' found. Replacing from backup...")
        conn.close()
        if not run_backup():
            return None

    except Error as e:
        if e.errno == 1049:
            if not run_backup():
                return None
        else:
            print(f"Connection error: {e}")
            return None

    try:
        conn = connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=DB_NAME
        )
        print(f"Connection established: {conn.server_host}")
        return conn
    except Error as e:
        print(f"Connection error after backup: {e}")
        return None


def load_dataframe():
    """Loads the poverty indicators CSV into a pandas DataFrame.

    If the ``tasa_desempleo`` (unemployment rate) column is not present,
    it is calculated from the employed and unemployed population columns.

    Returns:
        pandas.DataFrame: DataFrame with all indicator columns.
    """
    df = pd.read_csv(CSV_PATH)
    if 'tasa_desempleo' not in df.columns:
        df['tasa_desempleo'] = (
            df['pob_desocupada'] / (df['pob_ocupada'] + df['pob_desocupada'])
        ) * 100
    print(f"Dataframe loaded successfully — {len(df)} rows")
    return df


def insert(df):
    """Inserts all rows from the DataFrame into the database.

    Uses the global ``connection`` and ``cursor`` objects. Each row is
    inserted across four tables via stored procedures in a single atomic
    transaction. On failure, only that row is rolled back and the error
    is logged, allowing remaining rows to continue.

    Stored procedures called per row:
        - ``sp_insert_period``    → period
        - ``sp_insert_education`` → education_indicator
        - ``sp_insert_economy``   → economy_indicator
        - ``sp_insert_employment``→ employment_indicator

    Args:
        df (pandas.DataFrame): DataFrame returned by ``load_dataframe()``.
    """
    rows_ok = 0
    rows_err = 0

    for index, row in df.iterrows():
        try:
            # 1. Period — insert year and retrieve generated id_period
            cursor.callproc('sp_insert_period', (int(row['año']),))
            id_period = None
            for result in cursor.stored_results():
                r = result.fetchone()
                if r:
                    id_period = r[0]

            if id_period is None:
                raise ValueError(f"sp_insert_period returned no id for year {int(row['año'])}")

            # 2. Education indicators
            cursor.callproc('sp_insert_education', (
                int(id_period),
                float(row['anos_escolaridad_esp']),
                float(row['tasa_alfabetizacion']),
                float(row['gasto_educacion'])
            ))
            for _ in cursor.stored_results():
                pass

            # 3. Economy indicators
            cursor.callproc('sp_insert_economy', (
                int(id_period),
                float(row['indice_gini']),
                float(row['ingreso_per_capita_ppp']),
                float(row['inflacion']),
                float(row['pib_por_trabajador']),
                float(row['tasa_pobreza']),
                float(row['gasto_salud'])
            ))
            for _ in cursor.stored_results():
                pass

            # 4. Employment indicators
            cursor.callproc('sp_insert_employment', (
                int(id_period),
                int(row['pob_ocupada']),
                int(row['pob_desocupada']),
                int(row['poblacion_total']),
                float(row['tasa_actividad_laboral']),
                float(row['tasa_desempleo'])
            ))
            for _ in cursor.stored_results():
                pass

            connection.commit()
            rows_ok += 1
            print(f"  [OK] Year {int(row['año'])} inserted (id_period={id_period})")

        except Error as e:
            connection.rollback()
            rows_err += 1
            print(f"  [ERROR] Row {index} (year {row.get('año', '?')}): {e}")

        except Exception as e:
            connection.rollback()
            rows_err += 1
            print(f"  [ERROR] Row {index} (year {row.get('año', '?')}): {e}")

    print(f"\nProcess complete — {rows_ok} rows inserted, {rows_err} errors.")


# ── Global configuration ───────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_config = load_config(os.path.join(BASE_DIR, '..', 'config.txt'))
DB_NAME = db_config.get('database', 'pobreza')
BACKUP_PATH = os.path.join(BASE_DIR, 'DataBaseBackup.sql')
CSV_PATH = os.path.join(BASE_DIR, '..', 'DataExtraction', 'df_pobreza.csv')

# ── Global connection ──────────────────────────────────────────────────────────
connection = open_connection()

if connection is None:
    print("Could not connect to the database.")
else:
    cursor = connection.cursor()
    df = load_dataframe()
    insert(df)
    cursor.close()
    connection.close()