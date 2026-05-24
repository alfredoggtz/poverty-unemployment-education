"""
InsertMySQL.py
-----------------
Loads poverty-related indicators from a CSV file and inserts them into
a MySQL database using stored procedures. If the target database does
not exist, it is automatically recreated from a SQL backup file.

Dependencies: pandas, mysql-connector-python
Configuration: config.txt (see config.example.txt)
"""

import os
import subprocess
import pandas as pd
from mysql.connector import connect, Error


def cargar_config(ruta):
    """
    Reads database connection settings from a plain-text config file.

    Each line must follow the format: key=value
    Blank lines and lines without '=' are ignored.

    Args:
        ruta (str): Path to the config file.

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
db_config = cargar_config(os.path.join(BASE_DIR, '..', 'config.txt'))


def conectar():
    """
    Establishes a connection to the MySQL database.

    Before connecting, checks whether the target database exists.
    If it does not, the database is recreated by executing the SQL
    backup file (DataBaseBackup.sql) via the mysql CLI.

    Returns:
        mysql.connector.connection.MySQLConnection | None:
            An open connection on success, or None on failure.
    """
    try:
        # Connect without specifying the database to check if it exists
        conexion_temp = connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password']
        )
        cursor = conexion_temp.cursor()

        # Check if the target database exists
        cursor.execute(f"SHOW DATABASES LIKE '{db_config['database']}'")
        existe = cursor.fetchone()

        if not existe:
            print(f"Database '{db_config['database']}' not found. Creating from backup...")

            # Resolve the backup file path relative to this script's directory
            ruta_sql = os.path.join(BASE_DIR, 'DataBaseBackup.sql')

            # Execute the SQL backup using the mysql CLI
            # The backup must be generated with: mysqldump --no-data --databases --routines
            subprocess.run(
                [db_config['mysql_path'], f"-u{db_config['user']}", f"-p{db_config['password']}"],
                input=open(ruta_sql).read(),
                text=True
            )
            print("Database created successfully.")

        cursor.close()
        conexion_temp.close()

        # Connect normally to the database
        db_conexion = connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database']
        )
        print(f"Connection established: {db_conexion.server_host}")
        return db_conexion

    except Error as e:
        print(f"Connection error: {e}")
        return None


def obtener_df():
    """
    Loads the poverty indicators CSV into a pandas DataFrame.

    If the 'tasa_desempleo' (unemployment rate) column is not present,
    it is calculated from the employed and unemployed population columns.

    Returns:
        pandas.DataFrame: DataFrame with all indicator columns.
    """
    df = pd.read_csv('../DataExtraction/df_pobreza.csv')

    # Calculate unemployment rate only if it doesn't already exist in the CSV
    if 'tasa_desempleo' not in df.columns:
        df['tasa_desempleo'] = (
            df['pob_desocupada'] / (df['pob_ocupada'] + df['pob_desocupada'])
        ) * 100

    print(f"Dataframe loaded successfully — {len(df)} rows")
    return df


def insertar(df):
    """
    Inserts all rows from the DataFrame into the database.

    Each row is inserted across four tables using stored procedures:
        - sp_insert_period     → period
        - sp_insert_education  → education_indicator
        - sp_insert_economy    → economy_indicator
        - sp_insert_employment → employment_indicator

    Each row is committed as a single transaction. On failure,
    the transaction is rolled back and the error is logged,
    allowing remaining rows to continue processing.

    Args:
        df (pandas.DataFrame): DataFrame returned by obtener_df().
    """
    conexion = conectar()
    if conexion is None:
        print('Could not connect to the database.')
        return

    cursor = conexion.cursor()
    rows_ok = 0
    rows_err = 0

    for indice, fila in df.iterrows():
        try:
            # ── 1. Period ───────────────────────────────────────────────────
            # Insert the year and retrieve the generated id_period,
            # which is used as a foreign key in the three indicator tables
            cursor.callproc('sp_insert_period', (int(fila['año']),))

            id_period = None
            for result in cursor.stored_results():
                row = result.fetchone()
                if row:
                    id_period = row[0]

            if id_period is None:
                raise ValueError(f"sp_insert_period returned no id for year {int(fila['año'])}")

            # ── 2. Education ────────────────────────────────────────────────
            cursor.callproc('sp_insert_education', (
                int(id_period),
                float(fila['anos_escolaridad_esp']),
                float(fila['tasa_alfabetizacion']),
                float(fila['gasto_educacion'])
            ))
            # Consume stored results to avoid "commands out of sync" errors
            for _ in cursor.stored_results():
                pass

            # ── 3. Economy ──────────────────────────────────────────────────
            cursor.callproc('sp_insert_economy', (
                int(id_period),
                float(fila['indice_gini']),
                float(fila['ingreso_per_capita_ppp']),
                float(fila['inflacion']),
                float(fila['pib_por_trabajador']),
                float(fila['tasa_pobreza']),
                float(fila['gasto_salud'])
            ))
            for _ in cursor.stored_results():
                pass

            # ── 4. Employment ───────────────────────────────────────────────
            cursor.callproc('sp_insert_employment', (
                int(id_period),
                int(fila['pob_ocupada']),
                int(fila['pob_desocupada']),
                int(fila['poblacion_total']),
                float(fila['tasa_actividad_laboral']),
                float(fila['tasa_desempleo'])
            ))
            for _ in cursor.stored_results():
                pass

            # Commit all four inserts as a single atomic transaction
            conexion.commit()
            rows_ok += 1
            print(f"  [OK] Year {int(fila['año'])} inserted (id_period={id_period})")

        except Error as e:
            # Rollback the current row's transaction on database error
            conexion.rollback()
            rows_err += 1
            print(f"  [ERROR] Row {indice} (year {fila.get('año', '?')}): {e}")

        except Exception as e:
            # Rollback on any other unexpected error
            conexion.rollback()
            rows_err += 1
            print(f"  [ERROR] Row {indice} (year {fila.get('año', '?')}): {e}")

    cursor.close()
    conexion.close()
    print(f"\nProcess complete — {rows_ok} rows inserted, {rows_err} errors.")


if __name__ == '__main__':
    df = obtener_df()
    insertar(df)