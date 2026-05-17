import streamlit as st
import plotly.express as px

from data.loader import load_data


def render():
    st.set_page_config(page_title="Tendencias", layout="wide")

    df = load_data()

    st.title("📈 Tendencias Nacionales")

    # Filtros
    año_min, año_max = int(df["año"].min()), int(df["año"].max())
    rango = st.sidebar.slider("Rango de años", año_min, año_max, (año_min, año_max))

    dff = df[(df["año"] >= rango[0]) & (df["año"] <= rango[1])]

    # KPIs
    st.markdown("### 📌 Indicadores más recientes")
    ultimo = dff.iloc[-1]
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Tasa de desempleo", f"{ultimo['tasa_desempleo']:.1f}%")
    col2.metric("Índice Gini", f"{ultimo['indice_gini']:.1f}")
    col3.metric("Ingreso per cápita", f"${ultimo['ingreso_per_capita_ppp']:,.0f}")
    col4.metric("Alfabetización", f"{ultimo['tasa_alfabetizacion']:.1f}%")

    st.markdown("---")

    col1, col2 = st.columns(2)

    fig1 = px.line(dff, x="año", y="indice_gini",
                   title="Índice Gini a lo largo del tiempo",
                   markers=True, labels={"año": "Año", "indice_gini": "Índice Gini"})
    col1.plotly_chart(fig1, use_container_width=True)

    fig2 = px.area(dff, x="año", y="tasa_desempleo",
                   title="Tasa de Desempleo (%)",
                   labels={"año": "Año", "tasa_desempleo": "Desempleo (%)"})
    col2.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)

    fig3 = px.line(dff, x="año", y="ingreso_per_capita_ppp",
                   title="Ingreso per cápita PPP (USD)",
                   markers=True, labels={"año": "Año", "ingreso_per_capita_ppp": "USD"})
    col3.plotly_chart(fig3, use_container_width=True)

    fig4 = px.line(dff, x="año", y=["tasa_alfabetizacion", "anos_escolaridad_esp"],
                   title="Indicadores Educativos",
                   markers=True,
                   labels={"año": "Año", "value": "Valor", "variable": "Indicador"})
    col4.plotly_chart(fig4, use_container_width=True)

    st.markdown("---")
    st.markdown("### 👥 Población Ocupada vs Desocupada")

    fig5 = px.bar(dff, x="año", y=["pob_ocupada", "pob_desocupada"],
                  barmode="group", title="Población por condición de empleo",
                  labels={"año": "Año", "value": "Personas", "variable": "Condición"})
    st.plotly_chart(fig5, use_container_width=True)

    st.markdown("---")

    with st.expander("Ver datos"):
        st.dataframe(dff)

render()