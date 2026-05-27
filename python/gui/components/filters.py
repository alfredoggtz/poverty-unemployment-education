import streamlit as st
import pandas as pd

def render_filters(df: pd.DataFrame):
    st.sidebar.title("🎛️ Filtros")

    year_min = int(df['año'].min())
    year_max = int(df['año'].max())

    rango = st.sidebar.slider(
        "Rango de años",
        min_value=year_min,
        max_value=year_max,
        value=st.session_state.get("rango", (year_min, year_max)),
        step=1
    )
    st.session_state.rango = rango