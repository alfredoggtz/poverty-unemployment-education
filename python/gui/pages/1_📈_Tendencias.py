import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from data.loader import load_data
from components.filters import render_filters

st.set_page_config(page_title="Tendencias Globales", layout="wide")

df = load_data()
render_filters(df)
rango = st.session_state.get("rango", (int(df['año'].min()), int(df['año'].max())))

st.markdown("## 📈 Tendencias Globales")
st.markdown(f"Período: **{rango[0]} – {rango[1]}** · {rango[1] - rango[0] + 1} años")
st.markdown("---")

df_f = df[(df['año'] >= rango[0]) & (df['año'] <= rango[1])].copy()

# ── Métricas rápidas ──────────────────────────────────────────────────────────
st.markdown("### 📌 Resumen del período")

metrics = [
    ("Tasa de Pobreza",     "tasa_pobreza",          "%"),
    ("Tasa de Desempleo",   "tasa_desempleo",         "%"),
    ("Índice de Gini",      "indice_gini",            ""),
    ("Ingreso per Cápita",  "ingreso_per_capita_ppp", "USD"),
]

cols = st.columns(4)
for col, (label, campo, unidad) in zip(cols, metrics):
    inicio = df_f[campo].iloc[0]
    fin    = df_f[campo].iloc[-1]
    delta  = fin - inicio
    col.metric(
        label=label,
        value=f"{fin:,.1f} {unidad}".strip(),
        delta=f"{delta:+.1f} vs {rango[0]}"
    )

st.markdown("---")

# ── Gráfica 1: Pobreza · Desempleo · Actividad laboral (mismo eje %) ──────────
st.markdown("### 📊 Pobreza, desempleo y actividad laboral")
st.caption("Las tres variables están en porcentaje — comparación directa en el mismo eje.")

fig1 = go.Figure()
series_pda = [
    ("tasa_pobreza",           "Tasa de Pobreza (%)",          "#E24B4A"),
    ("tasa_desempleo",         "Tasa de Desempleo (%)",         "#378ADD"),
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

# ── Gráfica 2: Gini vs Pobreza (scatter por año) ──────────────────────────────
st.markdown("### 🔵 Desigualdad vs Pobreza")
st.caption("Cada punto es un año. ¿A mayor desigualdad (Gini), mayor pobreza?")

fig2 = px.scatter(
    df_f,
    x='indice_gini', y='tasa_pobreza',
    text='año',
    trendline='ols',
    labels={
        'indice_gini':   'Índice de Gini',
        'tasa_pobreza':  'Tasa de Pobreza (%)',
    },
    color_discrete_sequence=["#7F77DD"],
)
fig2.update_traces(textposition='top center', marker=dict(size=8))
fig2.update_layout(height=400, margin=dict(t=20, b=40))
st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ── Gráfica 3: Ingreso per cápita vs PIB por trabajador (eje doble) ───────────
st.markdown("### 💰 Ingreso per cápita y productividad")
st.caption(
    "Eje izquierdo = Ingreso per cápita PPP (USD · escala 13k–26k). "
    "Eje derecho = PIB por trabajador (USD · escala 48k–53k). "
    "Distintas magnitudes — cada una con su propia escala."
)

fig3 = go.Figure()
fig3.add_trace(go.Scatter(
    x=df_f['año'], y=df_f['ingreso_per_capita_ppp'],
    mode='lines+markers', name='Ingreso per Cápita PPP (USD)',
    line=dict(color="#BA7517", width=2),
    marker=dict(size=5),
    yaxis='y1'
))
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
    yaxis2=dict(title="PIB por Trabajador (USD)", overlaying='y', side='right', tickformat=","),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    margin=dict(t=40, b=40)
)
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# ── Tabla opcional ─────────────────────────────────────────────────────────────
with st.expander("🗃️ Ver datos del período"):
    cols_show = ['año', 'tasa_pobreza', 'tasa_desempleo', 'tasa_actividad_laboral',
                 'indice_gini', 'ingreso_per_capita_ppp', 'pib_por_trabajador']
    rename = {
        'tasa_pobreza':           'Pobreza (%)',
        'tasa_desempleo':         'Desempleo (%)',
        'tasa_actividad_laboral': 'Actividad Laboral (%)',
        'indice_gini':            'Gini',
        'ingreso_per_capita_ppp': 'Ingreso PPP (USD)',
        'pib_por_trabajador':     'PIB/Trabajador (USD)',
    }
    st.dataframe(
        df_f[cols_show].rename(columns=rename).set_index('año'),
        use_container_width=True
    )
    csv = df_f[cols_show].rename(columns=rename).to_csv(index=False).encode('utf-8')
    st.download_button(
        "⬇️ Descargar CSV", data=csv,
        file_name=f"tendencias_{rango[0]}_{rango[1]}.csv", mime="text/csv"
    )