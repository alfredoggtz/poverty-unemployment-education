import streamlit as st
import pandas as pd
import os

@st.cache_data
def load_data():
    base = os.path.dirname(os.path.abspath(__file__))
    ruta = os.path.join(base, '..', '..', 'DataExtraction', 'df_pobreza.csv')
    df = pd.read_csv(ruta)
    df['año'] = df['año'].astype(int)
    return df