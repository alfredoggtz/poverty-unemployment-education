import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

def load_data():
    csv_path = BASE_DIR / "df_pobreza.csv"
    df_gui = pd.read_csv(csv_path)
    df_gui["tasa_desempleo"] = (
        df_gui["pob_desocupada"] / (df_gui["pob_ocupada"] + df_gui["pob_desocupada"])
    ) * 100

    return df_gui