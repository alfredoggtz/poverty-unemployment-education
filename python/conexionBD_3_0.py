import pandas as pd
from mysql.connector import connect, Error

db_config = {
    'user'     : 'root',
    'host'     : 'localhost',
    'database' : 'pobreza',
    'password' : 'AlfGal2003'
}


def conectar():
    try:
        db_conexion = connect(
            host     = db_config['host'],
            user     = db_config['user'],
            password = db_config['password'],
            database = db_config['database']
        )
        print(f"Conexión establecida: {db_conexion.server_host}")
        return db_conexion
    except Error as e:
        print(f"Error al conectar: {e}")
        return None


def obtener_df():
    df = pd.read_csv('df_pobreza.csv')

    # Calcular tasa_desempleo solo si no existe ya en el CSV
    if 'tasa_desempleo' not in df.columns:
        df['tasa_desempleo'] = (
            df['pob_desocupada'] / (df['pob_ocupada'] + df['pob_desocupada'])
        ) * 100

    print(f"Dataframe cargado correctamente — {len(df)} filas")
    return df


def insertar(df):
    conexion = conectar()
    if conexion is None:
        print('No se pudo conectar a la base de datos.')
        return

    cursor = conexion.cursor()
    filas_ok  = 0
    filas_err = 0

    for indice, fila in df.iterrows():
        try:
            # ── 1. Periodo ──────────────────────────────────────────────────
            cursor.callproc('sp_insert_period', (int(fila['año']),))

            id_period = None
            for result in cursor.stored_results():
                row = result.fetchone()
                if row:
                    id_period = row[0]

            if id_period is None:
                raise ValueError(f"sp_insert_period no devolvió id para año {int(fila['año'])}")

            # ── 2. Educación ────────────────────────────────────────────────
            cursor.callproc('sp_insert_education', (
                int(id_period),
                float(fila['anos_escolaridad_esp']),
                float(fila['tasa_alfabetizacion']),
                float(fila['gasto_educacion'])
            ))
            for _ in cursor.stored_results():
                pass

            # ── 3. Economía ─────────────────────────────────────────────────
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

            # ── 4. Empleo ───────────────────────────────────────────────────
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

            conexion.commit()
            filas_ok += 1
            print(f"  [OK] Año {int(fila['año'])} insertado (id_period={id_period})")

        except Error as e:
            conexion.rollback()
            filas_err += 1
            print(f"  [ERROR] Fila {indice} (año {fila.get('año', '?')}): {e}")

        except Exception as e:
            conexion.rollback()
            filas_err += 1
            print(f"  [ERROR] Fila {indice} (año {fila.get('año', '?')}): {e}")

    cursor.close()
    conexion.close()
    print(f"\nProceso finalizado — {filas_ok} filas insertadas, {filas_err} errores.")


if __name__ == '__main__':
    df = obtener_df()
    insertar(df)