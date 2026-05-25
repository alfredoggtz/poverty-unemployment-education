import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import plotly.express as px

from components.filters import render_filters
from data.loader import load_data


def render():
    st.title("Empleo & Economía")

    df = load_data()
    render_filters(df)

    año_ini, año_fin = st.session_state.rango
    df_f = df[(df['año'] >= año_ini) & (df['año'] <= año_fin)]

    # ── Métricas ──────────────────────────────────────────────────────
    st.markdown("### Indicadores")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Pob. Ocupada Promedio", f"{df_f['pob_ocupada'].mean():,.0f}")
    col2.metric("Pob. Desocupada Promedio", f"{df_f['pob_desocupada'].mean():,.0f}")
    col3.metric("Tasa Actividad Laboral", f"{df_f['tasa_actividad_laboral'].mean():.1f}%")
    col4.metric("PIB por Trabajador Promedio", f"${df_f['pib_por_trabajador'].mean():,.0f}")

    st.markdown("---")

    col1, col2 = st.columns(2)

    df_pob = df_f[['año', 'pob_ocupada', 'pob_desocupada']].melt(
        id_vars='año', var_name='Tipo', value_name='Población'
    )
    fig1 = px.bar(
        df_pob, x='año', y='Población', color='Tipo', barmode='group',
        title='Población Ocupada vs Desocupada',
        labels={'año': 'Año', 'Población': 'Personas'}
    )
    col1.plotly_chart(fig1, use_container_width=True)

    fig2 = px.line(
        df_f, x='año', y='pib_por_trabajador',
        title='PIB por Trabajador por Año',
        markers=True, labels={'pib_por_trabajador': 'PIB por Trabajador (USD)', 'año': 'Año'}
    )
    col2.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)

    fig3 = px.area(
        df_f, x='año', y='tasa_actividad_laboral',
        title='Tasa de Actividad Laboral',
        labels={'tasa_actividad_laboral': 'Tasa (%)', 'año': 'Año'}
    )
    col3.plotly_chart(fig3, use_container_width=True)

    fig4 = px.scatter(
        df_f, x='inflacion', y='tasa_desempleo', text='año',
        title='Inflación vs Tasa de Desempleo',
        labels={'inflacion': 'Inflación (%)', 'tasa_desempleo': 'Desempleo (%)'}
    )
    fig4.update_traces(textposition='top center')
    col4.plotly_chart(fig4, use_container_width=True)

    st.markdown("### Desigualdad vs Ingreso")
    fig5 = px.scatter(
        df_f, x='ingreso_per_capita_ppp', y='indice_gini', text='año',
        title='Ingreso per Cápita vs Índice de Gini',
        labels={'ingreso_per_capita_ppp': 'Ingreso per Cápita (USD PPP)', 'indice_gini': 'Índice Gini'},
        trendline='ols'
    )
    fig5.update_traces(textposition='top center')
    st.plotly_chart(fig5, use_container_width=True)

    with st.expander("Ver Datos"):
        st.dataframe(df_f)


render()