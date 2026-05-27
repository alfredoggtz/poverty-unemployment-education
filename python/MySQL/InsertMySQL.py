"""
InsertMySQL.py
-----------------
Loads poverty-related indicators from a CSV file and inserts them into
a MySQL database using stored procedures. If the target database does
not exist, it is automatically recreated from the SQL backup file
using mysql.connector — no external CLI required.

Dependencies: pandas, mysql-connector-python
Configuration: config.txt (one level above this script's directory)
"""

import os
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


def run_sql_file(conn, path):
    """Executes all statements in a SQL file using an existing connection.

    Handles ``DELIMITER`` directives produced by mysqldump, which are
    needed for stored procedures and triggers but are not understood by
    mysql.connector directly.

    Args:
        conn: An open mysql.connector connection.
        path (str): Absolute path to the SQL file to execute.
    """
    cursor = conn.cursor()
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    delimiter = ';'
    current = []

    for line in content.splitlines():
        stripped = line.strip()

        # Handle DELIMITER changes (e.g. DELIMITER ;; or DELIMITER ;)
        if stripped.upper().startswith('DELIMITER'):
            new_delim = stripped.split()[1]
            # Execute any accumulated statement before switching delimiter
            statement = '\n'.join(current).strip()
            if statement:
                try:
                    cursor.execute(statement)
                    cursor.fetchall()
                except Error:
                    pass
            current = []
            delimiter = new_delim
            continue

        # Check if the current line ends with the active delimiter
        if stripped.endswith(delimiter):
            current.append(line[:line.rfind(delimiter)])
            statement = '\n'.join(current).strip()
            if statement:
                try:
                    cursor.execute(statement)
                    cursor.fetchall()
                except Error:
                    pass
            current = []
        else:
            current.append(line)

    # Execute any remaining statement
    statement = '\n'.join(current).strip()
    if statement:
        try:
            cursor.execute(statement)
            cursor.fetchall()
        except Error:
            pass

    conn.commit()
    cursor.close()


def run_backup():
    """Recreates the database by executing DataBaseBackup.sql.

    Connects without selecting a database and runs the backup file,
    which includes the schema, triggers, stored procedures, and views.

    Returns:
        bool: True if the backup executed successfully, False otherwise.
    """
    try:
        conn = connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password']
        )
        print(f"Executing: {os.path.basename(BACKUP_PATH)}")
        run_sql_file(conn, BACKUP_PATH)
        conn.close()
        print("Database created successfully.")
        return True

    except Error as e:
        print(f"[ERROR] Could not execute backup: {e}")
        return False


def open_connection():
    """Opens and returns a global MySQL connection, recreating the DB if needed.

    Attempts to connect directly to the target database. If it does not
    exist (error 1049), runs the SQL backup via mysql.connector and retries.
    If the database already exists, it is also replaced from backup to
    ensure a clean state before insertion.

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
            print(f"Database '{DB_NAME}' not found. Creating from backup...")
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