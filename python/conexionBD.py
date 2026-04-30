import pandas as pd
from mysql.connector import connect, Error

db_config = {
    'user' : 'samir',
    'host' : 'localhost',
    'database' : 'pobreza',
    'password' : '12345678'
}


def conectar():
    try:
        db_conexion = connect(host=db_config['host'],user=db_config['user'],
                              password=db_config['password'],database=db_config['database'])
        print(db_conexion)
        return(db_conexion)
    except Error as e:
        print(e)

def obtener_df():
    df = pd.read_csv('df_pobreza.csv')
    df['tasa_desempleo']= (df['pob_desocupada']/(df['pob_ocupada'] + df['pob_desocupada'])) *100
    print('Dataframe correctamente cargado')
    return df

def insertar(df):
    conexion = conectar()
    if conexion is None:
        print('No se pudo conectar')
        return
    if conexion.is_connected():
        cursor = conexion.cursor()
        # For para recorrer e insertar
        for indice, fila in df.iterrows():
            # Tabla periodo
            sql_year = 'INSERT INTO period (year_) VALUES (%s)'
            cursor.execute(sql_year, (int(fila['año']),))
            id_period = cursor.lastrowid  # Captura el ID recién insertado

            # Tabla indicador_educacion
            sql_education = 'INSERT INTO education_indicator (id_period, average_years_of_schooling, literacy_rate)VALUES (%s, %s, %s)'
            cursor.execute(sql_education,(id_period, fila['anos_escolaridad_esp'], fila['tasa_alfabetizacion']))

            # Tabla indicador_economia
            sql_economy = 'INSERT INTO economy_indicator (id_period, gini_index, per_capita_income) VALUES (%s, %s, %s)'
            cursor.execute(sql_economy, (id_period, fila['indice_gini'], fila['ingreso_per_capita_ppp']))

            # Tabla indicador_empleo
            sql_employment = 'INSERT INTO employment_indicator (id_period, employed_population, unemployed_population,unemployment_rate) VALUES (%s, %s, %s, %s)'
            cursor.execute(sql_employment, (id_period, fila['pob_ocupada'], fila['pob_desocupada'], fila['tasa_desempleo']))

        conexion.commit()
        cursor.close()
        conexion.close()
        print('Proceso con éxito, datos insertados correctamente')

if __name__ == '__main__':
    df = obtener_df()
    insertar(df)