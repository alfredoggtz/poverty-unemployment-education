"""«Tendencias Globales» page of the socioeconomic indicators dashboard.

This module defines one page of the multipage Streamlit application. It shows
the time evolution of the main socioeconomic indicators (poverty, unemployment,
inequality and income) within the year range selected by the user through the
sidebar filters.

The page renders top to bottom in the following order:

    1. Header with the period and the number of years analyzed.
    2. A row of four summary metrics, each with its variation (delta) relative
       to the first year of the period.
    3. A time series of poverty, unemployment and labor activity, all on a
       single percentage axis for direct comparison.
    4. A Gini vs. poverty scatter plot with an OLS trendline.
    5. A time series of income per capita and GDP per worker with a dual Y axis
       (different magnitudes, each with its own scale).
    6. An expandable table with the period's data and a CSV download button.

Project dependencies:
    data.loader.load_data: Returns the ``DataFrame`` with the indicators. It must
        include, at minimum, the columns used in this module (``año``,
        ``tasa_pobreza``, ``tasa_desempleo``, ``tasa_actividad_laboral``,
        ``indice_gini``, ``ingreso_per_capita_ppp`` and ``pib_por_trabajador``).
    components.filters.render_filters: Draws the filter controls and sets the
        year range in ``st.session_state``.

Third-party dependencies:
    streamlit, plotly. The OLS trendlines (``trendline='ols'``) additionally
    require the ``statsmodels`` package to be installed in the environment.

Session state (st.session_state):
    rango (tuple[int, int]): Start and end year selected in the filters. If the
        key does not exist, the full range of the ``DataFrame`` is used.

Usage example:
    This page is not run standalone; Streamlit loads it automatically from the
    ``pages/`` directory when the app is launched::

        streamlit run Inicio.py
"""

import sys, os

# Allows importing the project packages (``data``, ``components``) when the page
# runs from the ``pages/`` subdirectory: the project root directory is appended
# to ``sys.path``.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from data.loader import load_data
from components.filters import render_filters

# Page configuration. Must be the first Streamlit call in the script.
st.set_page_config(page_title="Tendencias Globales", layout="wide")

# Load the dataset and render the sidebar filters.
df = load_data()
render_filters(df)

# Active year range. If the filters have not set it in the session yet, the full
# period available in the data is used by default.
rango = st.session_state.get("rango", (int(df['año'].min()), int(df['año'].max())))

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("## 📈 Tendencias Globales")
st.markdown(f"Período: **{rango[0]} – {rango[1]}** · {rango[1] - rango[0] + 1} años")
st.markdown("---")

# Data subset restricted to the selected range. Copied to avoid Pandas warnings
# when assigning over a view.
df_f = df[(df['año'] >= rango[0]) & (df['año'] <= rango[1])].copy()

# ── Quick metrics ─────────────────────────────────────────────────────────────
st.markdown("### 📌 Resumen del período")

# Each tuple describes a metric: (visible label, column, unit to display).
metrics = [
    ("Tasa de Pobreza", "tasa_pobreza", "%"),
    ("Tasa de Desempleo", "tasa_desempleo", "%"),
    ("Índice de Gini", "indice_gini", ""),
    ("Ingreso per Cápita", "ingreso_per_capita_ppp", "USD"),
]

# One column per metric. The delta compares the last value of the period against
# the first one (``iloc[-1]`` vs ``iloc[0]``), so the ``DataFrame`` must be
# sorted chronologically.
cols = st.columns(4)
for col, (label, campo, unidad) in zip(cols, metrics):
    inicio = df_f[campo].iloc[0]
    fin = df_f[campo].iloc[-1]
    delta = fin - inicio
    col.metric(
        label=label,
        value=f"{fin:,.1f} {unidad}".strip(),
        delta=f"{delta:+.1f} vs {rango[0]}"
    )

st.markdown("---")

# ── Chart 1: Poverty · Unemployment · Labor activity (same % axis) ────────────
# The three series share a unit (percentage), so they are plotted on a single Y
# axis to ease direct visual comparison.
st.markdown("### 📊 Pobreza, desempleo y actividad laboral")
st.caption("Las tres variables están en porcentaje — comparación directa en el mismo eje.")

fig1 = go.Figure()
# Each tuple defines a series: (column, legend name, line color).
series_pda = [
    ("tasa_pobreza", "Tasa de Pobreza (%)", "#E24B4A"),
    ("tasa_desempleo", "Tasa de Desempleo (%)", "#378ADD"),
    ("tasa_actividad_laboral", "Tasa de Actividad Laboral (%)", "#1D9E75"),
]
for campo, nombre, color in series_pda:
    fig1.add_trace(go.Scatter(
        x=df_f['año'], y=df_f[campo],
        mode='lines+markers', name=nombre,
        line=dict(color=color, width=2),
        marker=dict(size=5)
    ))
fig1.update_layout(
    height=400,
    xaxis_title="Año",
    yaxis_title="Porcentaje (%)",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    margin=dict(t=40, b=40)
)
st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

# ── Chart 2: Gini vs Poverty (scatter by year) ────────────────────────────────
# Scatter plot where each point is a year. The OLS trendline helps visualize the
# relationship between inequality and poverty.
st.markdown("### 🔵 Desigualdad vs Pobreza")
st.caption("Cada punto es un año. ¿A mayor desigualdad (Gini), mayor pobreza?")

fig2 = px.scatter(
    df_f,
    x='indice_gini', y='tasa_pobreza',
    text='año',                # Label each point with its year.
    trendline='ols',           # Ordinary least squares regression (requires statsmodels).
    labels={
        'indice_gini': 'Índice de Gini',
        'tasa_pobreza': 'Tasa de Pobreza (%)',
    },
    color_discrete_sequence=["#7F77DD"],
)
fig2.update_traces(textposition='top center', marker=dict(size=8))
fig2.update_layout(height=400, margin=dict(t=20, b=40))
st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ── Chart 3: Income per capita vs GDP per worker (dual axis) ──────────────────
# Both series use dollars but on different orders of magnitude, so two
# independent Y axes are used (``y1`` left, ``y2`` right).
st.markdown("### 💰 Ingreso per cápita y productividad")
st.caption(
    "Eje izquierdo = Ingreso per cápita PPP (USD · escala 13k–26k). "
    "Eje derecho = PIB por trabajador (USD · escala 48k–53k). "
    "Distintas magnitudes — cada una con su propia escala."
)

fig3 = go.Figure()
# Series on the left axis (y1): income per capita.
fig3.add_trace(go.Scatter(
    x=df_f['año'], y=df_f['ingreso_per_capita_ppp'],
    mode='lines+markers', name='Ingreso per Cápita PPP (USD)',
    line=dict(color="#BA7517", width=2),
    marker=dict(size=5),
    yaxis='y1'
))
# Series on the right axis (y2): GDP per worker (dashed line to visually
# distinguish it from the first axis).
fig3.add_trace(go.Scatter(
    x=df_f['año'], y=df_f['pib_por_trabajador'],
    mode='lines+markers', name='PIB por Trabajador (USD)',
    line=dict(color="#185FA5", width=2, dash='dash'),
    marker=dict(size=5),
    yaxis='y2'
))
fig3.update_layout(
    height=400,
    xaxis_title="Año",
    yaxis=dict(title="Ingreso per Cápita (USD)", tickformat=","),
    # ``overlaying='y'`` overlays the second axis on the first; ``side='right'``
    # places it on the right.
    yaxis2=dict(title="PIB por Trabajador (USD)", overlaying='y', side='right', tickformat=","),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    margin=dict(t=40, b=40)
)
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# ── Optional table ────────────────────────────────────────────────────────────
# Collapsible section with the raw data for the period and a download option.
with st.expander("🗃️ Ver datos del período"):
    # Columns to display and their renaming for a readable presentation.
    cols_show = ['año', 'tasa_pobreza', 'tasa_desempleo', 'tasa_actividad_laboral', 'indice_gini', 'ingreso_per_capita_ppp', 'pib_por_trabajador']
    rename = {
        'tasa_pobreza': 'Pobreza (%)',
        'tasa_desempleo': 'Desempleo (%)',
        'tasa_actividad_laboral': 'Actividad Laboral (%)',
        'indice_gini': 'Gini',
        'ingreso_per_capita_ppp': 'Ingreso PPP (USD)',
        'pib_por_trabajador': 'PIB/Trabajador (USD)',
    }
    st.dataframe(
        df_f[cols_show].rename(columns=rename).set_index('año'),
        use_container_width=True
    )
    # Export the same view to CSV (UTF-8 encoded) for the download.
    csv = df_f[cols_show].rename(columns=rename).to_csv(index=False).encode('utf-8')
    st.download_button(
        "⬇️ Descargar CSV", data=csv,
        file_name=f"tendencias_{rango[0]}_{rango[1]}.csv", mime="text/csv"
    )