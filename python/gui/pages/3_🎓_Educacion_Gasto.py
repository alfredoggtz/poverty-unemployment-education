"""«Educación & Gasto Social» page of the socioeconomic indicators dashboard.

This module defines one page of the multipage Streamlit application. It focuses
on education (schooling, literacy) and social spending (education and health as a
percentage of GDP), as well as their relationship with poverty and unemployment,
within the year range selected by the user in the sidebar filters.

The page renders top to bottom in the following order:

    1. Header with the period and the number of years analyzed.
    2. A row of four summary metrics (schooling, literacy, education spending and
       health spending), with their variation relative to the first year.
    3. A time series of inflation, education spending and health spending on a
       single percentage axis (comparable ranges).
    4. A time series of years of schooling and literacy with a dual Y axis.
    5. A grouped bar chart comparing education vs. health spending.
    6. Two side-by-side scatter plots: schooling vs. poverty and education
       spending vs. unemployment (point size = health spending), both with an
       OLS trendline.
    7. An expandable table with the period's data and a CSV download button.

Project dependencies:
    data.loader.load_data: Returns the ``DataFrame`` with the indicators. It must
        include, at minimum, the columns used in this module (``año``,
        ``anos_escolaridad_esp``, ``tasa_alfabetizacion``, ``gasto_educacion``,
        ``gasto_salud``, ``inflacion``, ``tasa_pobreza`` and ``tasa_desempleo``).
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
st.set_page_config(page_title="Educación & Gasto Social", layout="wide")

# Load the dataset and render the sidebar filters.
df = load_data()
render_filters(df)

# Active year range. If the filters have not set it in the session yet, the full
# period available in the data is used by default.
rango = st.session_state.get("rango", (int(df['año'].min()), int(df['año'].max())))

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("## 🎓 Educación & Gasto Social")
st.markdown(f"Período: **{rango[0]} – {rango[1]}** · {rango[1] - rango[0] + 1} años")
st.markdown("---")

# Data subset restricted to the selected range. Copied to avoid Pandas warnings
# when assigning over a view.
df_f = df[(df['año'] >= rango[0]) & (df['año'] <= rango[1])].copy()

# ── Quick metrics ─────────────────────────────────────────────────────────────
st.markdown("### 📌 Resumen del período")

# Each tuple describes a metric: (visible label, column, unit to display).
metrics = [
    ("Años de Escolaridad","anos_escolaridad_esp", "años"),
    ("Alfabetización","tasa_alfabetizacion", "%"),
    ("Gasto en Educación","gasto_educacion", "% PIB"),
    ("Gasto en Salud","gasto_salud","% PIB"),
]

# One column per metric. The delta compares the last value of the period against
# the first one; all values are shown with two decimals.
cols = st.columns(4)
for col, (label, campo, unidad) in zip(cols, metrics):
    inicio = df_f[campo].iloc[0]
    fin= df_f[campo].iloc[-1]
    delta = fin-inicio
    col.metric(
        label=label,
        value=f"{fin:.2f} {unidad}",
        delta=f"{delta:+.2f} vs {rango[0]}"
    )

st.markdown("---")

# ── Chart 1: Inflation · Education spending · Health spending (same % axis) ───
# The three series are in percentage and share similar ranges (~3–8%), so they
# are plotted on a single Y axis for direct comparison.
st.markdown("### 📊 Inflación y gasto social (% del PIB / %)")
st.caption(
    "Las tres variables están en porcentaje y tienen rangos similares (3–8%). "
    "Un solo eje Y permite compararlas directamente."
)

fig1 = go.Figure()
# Each tuple defines a series: (column, legend name, line color).
series_pct = [
    ("inflacion","Inflación (%)","#E24B4A"),
    ("gasto_educacion","Gasto en Educación (% PIB)","#378ADD"),
    ("gasto_salud","Gasto en Salud (% PIB)","#1D9E75"),
]
for campo, nombre, color in series_pct:
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

# ── Chart 2: Schooling vs Literacy (dual axis) ────────────────────────────────
# Years of schooling and literacy percentage have different units, so two
# independent Y axes are used (``y1`` left, ``y2`` right).
st.markdown("### 📚 Escolaridad y alfabetización")
st.caption(
    "Eje izquierdo = Años de escolaridad (12–15 años). "
    "Eje derecho = Tasa de alfabetización (91–96%). "
    "Unidades diferentes — cada una con su escala."
)

fig2 = go.Figure()
# Series on the left axis (y1): years of schooling.
fig2.add_trace(go.Scatter(
    x=df_f['año'], y=df_f['anos_escolaridad_esp'],
    mode='lines+markers', name='Años de Escolaridad',
    line=dict(color="#BA7517", width=2),
    marker=dict(size=5),
    yaxis='y1'
))
# Series on the right axis (y2): literacy rate (dashed line).
fig2.add_trace(go.Scatter(
    x=df_f['año'], y=df_f['tasa_alfabetizacion'],
    mode='lines+markers', name='Tasa de Alfabetización (%)',
    line=dict(color="#7F77DD", width=2, dash='dash'),
    marker=dict(size=5),
    yaxis='y2'
))
fig2.update_layout(
    height=400,
    xaxis_title="Año",
    yaxis=dict(title="Años de Escolaridad"),
    yaxis2=dict(title="Alfabetización (%)", overlaying='y', side='right'),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    margin=dict(t=40, b=40)
)
st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ── Chart 3: Education vs health spending (grouped bars) ──────────────────────
# Bars grouped by year that allow comparing, year by year, how much of GDP goes
# to each social spending category.
st.markdown("### 💰 Gasto en Educación vs Salud (% del PIB)")
st.caption("Barras agrupadas por año — fácil comparar cuánto se destina a cada rubro.")

# ``melt`` reshapes the columns to long format (one row per year and spending
# type) so that Plotly Express can group the bars by the ``Tipo`` category.
df_gasto = df_f[['año', 'gasto_educacion', 'gasto_salud']].melt(
    id_vars='año', var_name='Tipo', value_name='% del PIB'
)
df_gasto['Tipo'] = df_gasto['Tipo'].replace({
    'gasto_educacion': 'Educación',
    'gasto_salud': 'Salud',
})
fig3 = px.bar(
    df_gasto, x='año', y='% del PIB', color='Tipo', barmode='group',
    labels={'año': 'Año'},
    color_discrete_map={'Educación': '#378ADD', 'Salud': '#1D9E75'},
)
fig3.update_layout(
    height=380,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    margin=dict(t=40, b=40)
)
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# ── Charts 4 and 5: Correlations (2 columns) ──────────────────────────────────
# Two scatter plots placed side by side, each with its OLS trendline and points
# labeled by year.
st.markdown("### 🔗 Análisis de correlación")
corr_col1, corr_col2 = st.columns(2, gap="medium")

with corr_col1:
    # Schooling–poverty relationship.
    st.caption("Años de escolaridad vs Pobreza — ¿más educación, menos pobreza?")
    fig4 = px.scatter(
        df_f, x='anos_escolaridad_esp', y='tasa_pobreza', text='año',
        trendline='ols',  # Requires statsmodels.
        labels={
            'anos_escolaridad_esp': 'Años de Escolaridad',
            'tasa_pobreza': 'Pobreza (%)',
        },
        color_discrete_sequence=["#BA7517"],
    )
    fig4.update_traces(textposition='top center', marker=dict(size=7))
    fig4.update_layout(height=380, margin=dict(t=20, b=20))
    st.plotly_chart(fig4, use_container_width=True)

with corr_col2:
    # Education spending–unemployment relationship. The size of each point encodes
    # a third variable: health spending (``size='gasto_salud'``).
    st.caption("Gasto en educación vs Desempleo (tamaño = gasto en salud)")
    fig5 = px.scatter(
        df_f, x='gasto_educacion', y='tasa_desempleo', text='año',
        size='gasto_salud',
        trendline='ols',  # Requires statsmodels.
        labels={
            'gasto_educacion': 'Gasto Educación (% PIB)',
            'tasa_desempleo': 'Desempleo (%)',
        },
        color_discrete_sequence=["#1D9E75"],
    )
    fig5.update_traces(textposition='top center')
    fig5.update_layout(height=380, margin=dict(t=20, b=20))
    st.plotly_chart(fig5, use_container_width=True)

st.markdown("---")

# ── Optional table ────────────────────────────────────────────────────────────
# Collapsible section with the raw data for the period and a download option.
with st.expander("🗃️ Ver datos del período"):
    # Columns to display and their renaming for a readable presentation.
    cols_show = ['año', 'anos_escolaridad_esp', 'tasa_alfabetizacion', 'gasto_educacion', 'gasto_salud', 'inflacion', 'tasa_pobreza', 'tasa_desempleo']
    rename = {
        'anos_escolaridad_esp':'Escolaridad (años)',
        'tasa_alfabetizacion': 'Alfabetización (%)',
        'gasto_educacion':'Gasto Educación (% PIB)',
        'gasto_salud':'Gasto Salud (% PIB)',
        'inflacion':'Inflación (%)',
        'tasa_pobreza':'Pobreza (%)',
        'tasa_desempleo':'Desempleo (%)',
    }
    st.dataframe(
        df_f[cols_show].rename(columns=rename).set_index('año'),
        use_container_width=True
    )
    # Export the same view to CSV (UTF-8 encoded) for the download.
    csv = df_f[cols_show].rename(columns=rename).to_csv(index=False).encode('utf-8')
    st.download_button(
        "⬇️ Descargar CSV", data=csv,
        file_name=f"educacion_gasto_{rango[0]}_{rango[1]}.csv", mime="text/csv"
    )