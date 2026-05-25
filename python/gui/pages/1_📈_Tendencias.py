import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import plotly.express as px

from components.filters import render_filters
from data.loader import load_data


def render():
    st.set_page_config(page_title="Tendencias", layout="wide")
    st.title("Tendencias Globales")

    df = load_data()
    render_filters(df)

    año_ini, año_fin = st.session_state.rango
    df_f = df[(df['año'] >= año_ini) & (df['año'] <= año_fin)]

    # ── Indicadores ──────────────────────────────────────────────────
    st.markdown("### Indicadores Clave")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Tasa de Pobreza Promedio", f"{df_f['tasa_pobreza'].mean():.1f}%")
    col2.metric("Tasa de Desempleo Promedio", f"{df_f['tasa_desempleo'].mean():.1f}%")
    col3.metric("Índice Gini Promedio", f"{df_f['indice_gini'].mean():.1f}")
    col4.metric("Ingreso per Cápita Promedio", f"${df_f['ingreso_per_capita_ppp'].mean():,.0f}")

    st.markdown("---")

    # ── Líneas de tendencia principales ──────────────────────────────
    col1, col2 = st.columns(2)

    fig1 = px.line(
        df_f, x='año', y='tasa_pobreza',
        title='Tasa de Pobreza por Año',
        markers=True, labels={'tasa_pobreza': 'Tasa de Pobreza (%)', 'año': 'Año'}
    )
    col1.plotly_chart(fig1, use_container_width=True)

    fig2 = px.line(
        df_f, x='año', y='tasa_desempleo',
        title='Tasa de Desempleo por Año',
        markers=True, labels={'tasa_desempleo': 'Tasa de Desempleo (%)', 'año': 'Año'}
    )
    col2.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)

    fig3 = px.line(
        df_f, x='año', y='indice_gini',
        title='Índice de Gini por Año',
        markers=True, labels={'indice_gini': 'Índice Gini', 'año': 'Año'}
    )
    col3.plotly_chart(fig3, use_container_width=True)

    fig4 = px.area(
        df_f, x='año', y='ingreso_per_capita_ppp',
        title='Ingreso per Cápita (PPP) por Año',
        labels={'ingreso_per_capita_ppp': 'Ingreso per Cápita (USD)', 'año': 'Año'}
    )
    col4.plotly_chart(fig4, use_container_width=True)

    # ── Múltiples indicadores normalizados ────────────────────────────
    st.markdown("### Evolución Comparada")

    cols_norm = ['tasa_pobreza', 'tasa_desempleo', 'inflacion']
    df_norm = df_f[['año'] + cols_norm].copy()
    for col in cols_norm:
        min_v, max_v = df_norm[col].min(), df_norm[col].max()
        df_norm[col] = (df_norm[col] - min_v) / (max_v - min_v) if max_v != min_v else 0

    df_melted = df_norm.melt(id_vars='año', var_name='Indicador', value_name='Valor Normalizado')
    fig5 = px.line(
        df_melted, x='año', y='Valor Normalizado', color='Indicador',
        title='Pobreza, Desempleo e Inflación (Normalizado 0–1)',
        markers=True
    )
    st.plotly_chart(fig5, use_container_width=True)

    with st.expander("Ver Datos"):
        st.dataframe(df_f)


render()