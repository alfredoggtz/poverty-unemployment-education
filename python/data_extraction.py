import requests
import pandas as pd

token = "25d5cd4c-4f60-d8ea-bdd3-d030ed46aa68"
url_base = "https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/indicator"

inegi_indicadores = {
    "6200032092": "pob_desocupada",
    "6200093709": "pob_ocupada",
}

wb_indicadores = {
    "SI.POV.GINI":"indice_gini",
    "NY.GNP.PCAP.PP.CD": "ingreso_per_capita_ppp",
    "SE.ADT.LITR.ZS":"tasa_alfabetizacion",
    "SE.SCH.LIFE":"anos_escolaridad_esp",
    "SP.POP.TOTL":"poblacion_total",
    "SL.UEM.TOTL.ZS":"tasa_desempleo",
    "SL.GDP.PCAP.EM.KD":"pib_por_trabajador",
    "FP.CPI.TOTL.ZG":"inflacion",
    "SL.TLF.ACTI.ZS":"tasa_actividad_laboral",
    "SH.XPD.CHEX.GD.ZS":"gasto_salud",
    "SE.XPD.TOTL.GD.ZS":"gasto_educacion",
    "SI.POV.NAHC":"tasa_pobreza",
}

def obtener_inegi():
    print("inegi...")
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
                anio = int(obs["TIME_PERIOD"].split("/")[0])
                if obs.get("OBS_VALUE") is None:
                    continue
                valor = float(obs["OBS_VALUE"])
                registros.append({"año": anio, "variable": nombre, "valor": valor})
            except (ValueError, KeyError):
                continue

    return pd.DataFrame(registros)

def obtener_worldbank():
    print("world bank...")
    registros = []

    for codigo, nombre in wb_indicadores.items():
        url = f"https://api.worldbank.org/v2/country/MX/indicator/{codigo}?format=json&per_page=100"
        respuesta = requests.get(url)
        if respuesta.status_code != 200:
            print(f"error world bank {nombre}: {respuesta.status_code}")
            continue

        data = respuesta.json()
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
    todos_los_anios = pd.DataFrame({"año": range(2005, 2026)})
    df = todos_los_anios.merge(df, on="año", how="left")

    columnas_indicadores = [col for col in df.columns if col != "año"]
    for col in columnas_indicadores:
        df[col] = df[col].interpolate(method="linear", limit_direction="both") # esta madre es nueva  genera un valor intermedi

    return df


def construir_dataset():
    df_inegi = obtener_inegi()
    df_wb = obtener_worldbank()

    df_raw = pd.concat([df_inegi, df_wb], ignore_index=True)

    df = df_raw.groupby(["año", "variable"])["valor"].mean().unstack().reset_index()
    df.columns = [c.lower() for c in df.columns]

    df = df[df["año"].between(2005, 2025)].sort_values("año").reset_index(drop=True)
    df = rellenar_nulos(df)

    nombre_archivo = "df_pobreza.csv"
    df.to_csv(nombre_archivo, index=False)
    print(df.to_string(index=False))


if __name__ == "__main__":
    construir_dataset()
