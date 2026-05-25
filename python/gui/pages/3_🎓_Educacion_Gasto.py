import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import plotly.express as px
import statsmodels as sm

from components.filters import render_filters
from data.loader import load_data


def render():
    st.title("Educación & Gasto Social")

    df = load_data()
    render_filters(df)

    año_ini, año_fin = st.session_state.rango
    df_f = df[(df['año'] >= año_ini) & (df['año'] <= año_fin)]

    # ── Métricas ──────────────────────────────────────────────────────
    st.markdown("### Indicadores")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Años de Escolaridad Prom.", f"{df_f['anos_escolaridad_esp'].mean():.1f}")
    col2.metric("Tasa de Alfabetización Prom.", f"{df_f['tasa_alfabetizacion'].mean():.1f}%")
    col3.metric("Gasto en Educación Prom.", f"{df_f['gasto_educacion'].mean():.2f}% del PIB")
    col4.metric("Gasto en Salud Prom.", f"{df_f['gasto_salud'].mean():.2f}% del PIB")

    st.markdown("---")

    col1, col2 = st.columns(2)

    fig1 = px.line(
        df_f, x='año', y='anos_escolaridad_esp',
        title='Años de Escolaridad Esperados por Año',
        markers=True, labels={'anos_escolaridad_esp': 'Años', 'año': 'Año'}
    )
    col1.plotly_chart(fig1, use_container_width=True)

    fig2 = px.line(
        df_f, x='año', y='tasa_alfabetizacion',
        title='Tasa de Alfabetización por Año',
        markers=True, labels={'tasa_alfabetizacion': 'Tasa (%)', 'año': 'Año'}
    )
    col2.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)

    df_gasto = df_f[['año', 'gasto_educacion', 'gasto_salud']].melt(
        id_vars='año', var_name='Tipo', value_name='% del PIB'
    )
    fig3 = px.bar(
        df_gasto, x='año', y='% del PIB', color='Tipo', barmode='group',
        title='Gasto en Educación vs Salud (% del PIB)',
        labels={'año': 'Año'}
    )
    col3.plotly_chart(fig3, use_container_width=True)

    fig4 = px.scatter(
        df_f, x='anos_escolaridad_esp', y='tasa_pobreza', text='año',
        title='Años de Escolaridad vs Tasa de Pobreza',
        labels={'anos_escolaridad_esp': 'Años de Escolaridad', 'tasa_pobreza': 'Pobreza (%)'},
        trendline='ols'
    )
    fig4.update_traces(textposition='top center')
    col4.plotly_chart(fig4, use_container_width=True)

    st.markdown("### Gasto Social vs Resultados")
    fig5 = px.scatter(
        df_f, x='gasto_educacion', y='tasa_desempleo', text='año',
        size='gasto_salud',
        title='Gasto en Educación vs Desempleo (tamaño = gasto en salud)',
        labels={'gasto_educacion': 'Gasto Educación (% PIB)', 'tasa_desempleo': 'Desempleo (%)'},
        trendline='ols'
    )
    fig5.update_traces(textposition='top center')
    st.plotly_chart(fig5, use_container_width=True)

    with st.expander("Ver Datos"):
        cols = ['año', 'anos_escolaridad_esp', 'tasa_alfabetizacion', 'gasto_educacion', 'gasto_salud', 'tasa_pobreza']
        st.dataframe(df_f[cols])

    csv = df_f.to_csv(index=False).encode('utf-8')
    st.download_button("Descargar datos como CSV", data=csv, file_name="pobreza_filtrado.csv", mime="text/csv")


render()