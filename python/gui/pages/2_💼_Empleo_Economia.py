"""«Empleo & Economía» page of the socioeconomic indicators dashboard.

This module defines one page of the multipage Streamlit application. It focuses
on the labor market and its relationship with macroeconomic variables
(productivity, unemployment, inflation, income and inequality) within the year
range selected by the user in the sidebar filters.

The page renders top to bottom in the following order:

    1. Header with the period and the number of years analyzed.
    2. A row of four summary metrics (employed/unemployed population, GDP per
       worker and unemployment), with their variation relative to the first year.
    3. A stacked area chart of employed vs. unemployed population (same unit:
       people).
    4. A time series of GDP per worker and unemployment rate with a dual Y axis.
    5. Two side-by-side scatter plots: inflation vs. unemployment (Phillips
       curve) and income per capita vs. inequality, both with an OLS trendline.
    6. An expandable table with the period's data and a CSV download button.

Project dependencies:
    data.loader.load_data: Returns the ``DataFrame`` with the indicators. It must
        include, at minimum, the columns used in this module (``año``,
        ``pob_ocupada``, ``pob_desocupada``, ``poblacion_total``,
        ``pib_por_trabajador``, ``tasa_desempleo``, ``inflacion``,
        ``indice_gini`` and ``ingreso_per_capita_ppp``).
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
st.set_page_config(page_title="Empleo & Economía", layout="wide")

# Load the dataset and render the sidebar filters.
df = load_data()
render_filters(df)

# Active year range. If the filters have not set it in the session yet, the full
# period available in the data is used by default.
rango = st.session_state.get("rango", (int(df['año'].min()), int(df['año'].max())))

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("## 💼 Empleo & Economía")
st.markdown(f"Período: **{rango[0]} – {rango[1]}** · {rango[1] - rango[0] + 1} años")
st.markdown("---")

# Data subset restricted to the selected range. Copied to avoid Pandas warnings
# when assigning over a view.
df_f = df[(df['año'] >= rango[0]) & (df['año'] <= rango[1])].copy()

# ── Quick metrics ─────────────────────────────────────────────────────────────
st.markdown("### 📌 Resumen del período")

# Each tuple describes a metric: (visible label, column, unit to display).
# An empty unit denotes a people count, which is formatted with no decimals.
metrics = [
    ("Población Ocupada","pob_ocupada",""),
    ("Población Desocupada", "pob_desocupada",""),
    ("PIB por Trabajador","pib_por_trabajador","USD"),
    ("Tasa de Desempleo","tasa_desempleo","%"),
]

# One column per metric. The delta compares the last value of the period against
# the first one; the format changes with the unit (integers for people counts,
# one decimal for percentages and USD amounts).
cols = st.columns(4)
for col, (label, campo, unidad) in zip(cols, metrics):
    inicio = df_f[campo].iloc[0]
    fin    = df_f[campo].iloc[-1]
    delta  = fin - inicio
    if unidad == "":
        # People counts: thousands separator, no decimals.
        val_str = f"{fin:,.0f}"
        delta_str = f"{delta:+,.0f} vs {rango[0]}"
    else:
        # Percentages and amounts: one decimal and the corresponding unit.
        val_str = f"{fin:,.1f} {unidad}"
        delta_str = f"{delta:+.1f} vs {rango[0]}"
    col.metric(label=label, value=val_str, delta=delta_str)

st.markdown("---")

# ── Chart 1: Employed vs unemployed population (stacked area) ──────────────────
# Both series share a unit (people), so a stacked area shows both the total labor
# force and the unemployed share.
st.markdown("### 👥 Población ocupada vs desocupada")
st.caption("Área apilada — misma unidad (personas). Se aprecia cómo crece la fuerza laboral total y qué parte queda desocupada.")

# ``melt`` reshapes the columns to long format (one row per year and state) so
# that Plotly Express can color by the ``Estado`` category.
df_pob = df_f[['año', 'pob_ocupada', 'pob_desocupada']].melt(
    id_vars='año', var_name='Estado', value_name='Personas'
)
df_pob['Estado'] = df_pob['Estado'].replace({
    'pob_ocupada': 'Ocupada',
    'pob_desocupada': 'Desocupada',
})

fig1 = px.area(
    df_pob, x='año', y='Personas', color='Estado',
    labels={'año': 'Año', 'Personas': 'Personas'},
    color_discrete_map={'Ocupada': '#1D9E75', 'Desocupada': '#E24B4A'},
)
fig1.update_layout(
    height=400,
    yaxis_tickformat=",",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    margin=dict(t=40, b=40)
)
st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

# ── Chart 2: GDP per worker vs Unemployment rate (dual axis) ──────────────────
# Productivity (USD) and unemployment (%) have different units, so two
# independent Y axes are used (``y1`` left, ``y2`` right).
st.markdown("### 📉 Productividad vs Desempleo")
st.caption(
    "Eje izquierdo = PIB por trabajador (USD). "
    "Eje derecho = Tasa de desempleo (%). "
    "¿Cuando sube la productividad, baja el desempleo?"
)

fig2 = go.Figure()
# Series on the left axis (y1): GDP per worker.
fig2.add_trace(go.Scatter(
    x=df_f['año'], y=df_f['pib_por_trabajador'],
    mode='lines+markers', name='PIB por Trabajador (USD)',
    line=dict(color="#185FA5", width=2),
    marker=dict(size=5),
    yaxis='y1'
))
# Series on the right axis (y2): unemployment rate (dashed line).
fig2.add_trace(go.Scatter(
    x=df_f['año'], y=df_f['tasa_desempleo'],
    mode='lines+markers', name='Tasa de Desempleo (%)',
    line=dict(color="#E24B4A", width=2, dash='dash'),
    marker=dict(size=5),
    yaxis='y2'
))
fig2.update_layout(
    height=400,
    xaxis_title="Año",
    yaxis=dict(title="PIB por Trabajador (USD)", tickformat=","),
    yaxis2=dict(title="Desempleo (%)", overlaying='y', side='right'),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    margin=dict(t=40, b=40)
)
st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ── Charts 3 and 4: Correlations (2 columns) ──────────────────────────────────
# Two scatter plots placed side by side, each with its OLS trendline and points
# labeled by year.
st.markdown("### 🔗 Análisis de correlación")
corr_col1, corr_col2 = st.columns(2, gap="medium")

with corr_col1:
    # Inflation–unemployment relationship (Phillips curve hypothesis).
    st.caption("Inflación vs Desempleo — ¿relación de Phillips?")
    fig3 = px.scatter(
        df_f, x='inflacion', y='tasa_desempleo', text='año',
        trendline='ols',  # Requires statsmodels.
        labels={'inflacion':'Inflación (%)', 'tasa_desempleo': 'Desempleo (%)'},
        color_discrete_sequence=["#378ADD"],
    )
    fig3.update_traces(textposition='top center', marker=dict(size=7))
    fig3.update_layout(height=380, margin=dict(t=20, b=20))
    st.plotly_chart(fig3, use_container_width=True)

with corr_col2:
    # Income per capita–inequality relationship.
    st.caption("Ingreso per Cápita vs Desigualdad (Gini)")
    fig4 = px.scatter(
        df_f, x='ingreso_per_capita_ppp', y='indice_gini', text='año',
        trendline='ols',  # Requires statsmodels.
        labels={
            'ingreso_per_capita_ppp':'Ingreso per Cápita (USD PPP)',
            'indice_gini':'Índice de Gini',
        },
        color_discrete_sequence=["#7F77DD"],
    )
    fig4.update_traces(textposition='top center', marker=dict(size=7))
    fig4.update_layout(height=380, margin=dict(t=20, b=20))
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# ── Optional table ────────────────────────────────────────────────────────────
# Collapsible section with the raw data for the period and a download option.
with st.expander("🗃️ Ver datos del período"):
    # Columns to display and their renaming for a readable presentation.
    cols_show = ['año', 'pob_ocupada','pob_desocupada','poblacion_total', 'pib_por_trabajador','tasa_desempleo','inflacion', 'indice_gini', 'ingreso_per_capita_ppp']
    rename = {
        'pob_ocupada':'Pob. Ocupada',
        'pob_desocupada':'Pob. Desocupada',
        'poblacion_total':'Pob. Total',
        'pib_por_trabajador':'PIB/Trabajador (USD)',
        'tasa_desempleo':'Desempleo (%)',
        'inflacion':'Inflación (%)',
        'indice_gini':'Gini',
        'ingreso_per_capita_ppp':'Ingreso PPP (USD)',
    }
    st.dataframe(
        df_f[cols_show].rename(columns=rename).set_index('año'),
        use_container_width=True
    )
    # Export the same view to CSV (UTF-8 encoded) for the download.
    csv = df_f[cols_show].rename(columns=rename).to_csv(index=False).encode('utf-8')
    st.download_button(
        "⬇️ Descargar CSV", data=csv,
        file_name=f"empleo_economia_{rango[0]}_{rango[1]}.csv", mime="text/csv"
    )