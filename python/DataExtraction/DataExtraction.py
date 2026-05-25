"""
DataExtraction.py
------------------
Fetches poverty-related indicators for Mexico from two public APIs:
    - INEGI (Instituto Nacional de Estadística y Geografía)
    - World Bank

The data is merged, filtered for the 2005–2025 range, cleaned by
interpolating missing values, and exported as a CSV file (df_pobreza.csv).

Dependencies: requests, pandas
"""

import requests
import pandas as pd
import os

# INEGI API authentication token
token = "25d5cd4c-4f60-d8ea-bdd3-d030ed46aa68"
url_base = "https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/indicator"

# INEGI indicator IDs mapped to their column names in the final dataset
inegi_indicadores = {
    "6200032092": "pob_desocupada",
    "6200093709": "pob_ocupada",
}

# World Bank indicator codes mapped to their column names in the final dataset
wb_indicadores = {
    "SI.POV.GINI": "indice_gini",
    "NY.GNP.PCAP.PP.CD": "ingreso_per_capita_ppp",
    "SE.ADT.LITR.ZS": "tasa_alfabetizacion",
    "SE.SCH.LIFE": "anos_escolaridad_esp",
    "SP.POP.TOTL": "poblacion_total",
    "SL.UEM.TOTL.ZS": "tasa_desempleo",
    "SL.GDP.PCAP.EM.KD": "pib_por_trabajador",
    "FP.CPI.TOTL.ZG": "inflacion",
    "SL.TLF.ACTI.ZS": "tasa_actividad_laboral",
    "SH.XPD.CHEX.GD.ZS": "gasto_salud",
    "SE.XPD.TOTL.GD.ZS": "gasto_educacion",
    "SI.POV.NAHC": "tasa_pobreza",
}


def obtener_inegi():
    """
    Fetches employment indicators from the INEGI API.

    Requests all indicator IDs in a single call by joining them with commas.
    Parses the 'Series' structure in the response, extracting the year
    and observed value for each data point.

    Returns:
        pandas.DataFrame: Long-format DataFrame with columns:
            - año (int): observation year
            - variable (str): indicator name
            - valor (float): observed value
        Returns an empty DataFrame if the request fails.
    """
    print("inegi...")

    # Join all indicator IDs into a single comma-separated string for the API call
    ids = ",".join(inegi_indicadores.keys())
    url = f"{url_base}/{ids}/es/00/false/bise/2.0/{token}?type=json"

    respuesta = requests.get(url)
    if respuesta.status_code != 200:
        print(f"error inegi: {respuesta.status_code}")
        return pd.DataFrame()

    registros = []
    for serie in respuesta.json().get("Series", []):
        nombre = inegi_indicadores.get(serie["INDICADOR"], serie["INDICADOR"])
        for obs in serie["OBSERVATIONS"]:
            try:
                # TIME_PERIOD may be in 'YYYY/MM' format; extract only the year
                anio = int(obs["TIME_PERIOD"].split("/")[0])
                if obs.get("OBS_VALUE") is None:
                    continue
                valor = float(obs["OBS_VALUE"])
                registros.append({"año": anio, "variable": nombre, "valor": valor})
            except (ValueError, KeyError):
                continue

    return pd.DataFrame(registros)


def obtener_worldbank():
    """
    Fetches socioeconomic indicators for Mexico from the World Bank API.

    Makes one request per indicator. Skips indicators that return
    an error or an empty response.

    Returns:
        pandas.DataFrame: Long-format DataFrame with columns:
            - año (int): observation year
            - variable (str): indicator name
            - valor (float): observed value
        Returns an empty DataFrame if all requests fail.
    """
    print("world bank...")
    registros = []

    for codigo, nombre in wb_indicadores.items():
        url = f"https://api.worldbank.org/v2/country/MX/indicator/{codigo}?format=json&per_page=100"
        respuesta = requests.get(url)
        if respuesta.status_code != 200:
            print(f"error world bank {nombre}: {respuesta.status_code}")
            continue

        data = respuesta.json()

        # World Bank returns a two-element list: [metadata, records]
        # Skip if the response is malformed or the records list is empty
        if not data or len(data) < 2 or data[1] is None:
            continue

        for obs in data[1]:
            if obs.get("value") is None:
                continue
            registros.append({
                "año":      int(obs["date"]),
                "variable": nombre,
                "valor":    float(obs["value"])
            })

    return pd.DataFrame(registros)


def rellenar_nulos(df):
    """
    Fills missing values in the dataset using linear interpolation.

    Ensures all years from 2005 to 2025 are present by merging against
    a complete year range, then interpolates missing values for each
    indicator column in both forward and backward directions.

    Args:
        df (pandas.DataFrame): Wide-format DataFrame with 'año' as index column.

    Returns:
        pandas.DataFrame: DataFrame with no missing values for the 2005–2025 range.
    """
    todos_los_anios = pd.DataFrame({"año": range(2005, 2026)})

    # Left join ensures every year in the range is present, even if no data exists
    df = todos_los_anios.merge(df, on="año", how="left")

    columnas_indicadores = [col for col in df.columns if col != "año"]
    for col in columnas_indicadores:
        # linear interpolation fills gaps between known values;
        # limit_direction='both' also fills leading and trailing NaNs
        df[col] = df[col].interpolate(method="linear", limit_direction="both")

    return df


def construir_dataset():
    """
    Orchestrates the full data pipeline and exports the result to CSV.

    Steps:
        1. Fetch data from INEGI and World Bank.
        2. Concatenate both sources into a single long-format DataFrame.
        3. Pivot from long to wide format, averaging duplicates per year/variable.
        4. Filter to the 2005–2025 range and sort by year.
        5. Interpolate missing values.
        6. Export to 'df_pobreza.csv'.
    """
    df_inegi = obtener_inegi()
    df_wb = obtener_worldbank()

    df_raw = pd.concat([df_inegi, df_wb], ignore_index=True)

    df = df_raw.groupby(["año", "variable"])["valor"].mean().unstack().reset_index()
    df.columns = [c.lower() for c in df.columns]

    df = df[df["año"].between(2005, 2025)].sort_values("año").reset_index(drop=True)
    df = rellenar_nulos(df)

    # Save CSV relative to this script's directory
    nombre_archivo = os.path.join(os.path.dirname(__file__), 'df_pobreza.csv')
    df.to_csv(nombre_archivo, index=False)
    print(df.to_string(index=False))


if __name__ == "__main__":
    construir_dataset()