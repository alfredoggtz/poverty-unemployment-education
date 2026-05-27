import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from data.loader import load_data
from components.filters import render_filters

st.set_page_config(page_title="Empleo & Economía", layout="wide")

df = load_data()
render_filters(df)
rango = st.session_state.get("rango", (int(df['año'].min()), int(df['año'].max())))

st.markdown("## 💼 Empleo & Economía")
st.markdown(f"Período: **{rango[0]} – {rango[1]}** · {rango[1] - rango[0] + 1} años")
st.markdown("---")

df_f = df[(df['año'] >= rango[0]) & (df['año'] <= rango[1])].copy()

# ── Métricas rápidas ──────────────────────────────────────────────────────────
st.markdown("### 📌 Resumen del período")

metrics = [
    ("Población Ocupada","pob_ocupada",""),
    ("Población Desocupada", "pob_desocupada",""),
    ("PIB por Trabajador","pib_por_trabajador","USD"),
    ("Tasa de Desempleo","tasa_desempleo","%"),
]

cols = st.columns(4)
for col, (label, campo, unidad) in zip(cols, metrics):
    inicio = df_f[campo].iloc[0]
    fin    = df_f[campo].iloc[-1]
    delta  = fin - inicio
    if unidad == "":
        val_str   = f"{fin:,.0f}"
        delta_str = f"{delta:+,.0f} vs {rango[0]}"
    else:
        val_str   = f"{fin:,.1f} {unidad}"
        delta_str = f"{delta:+.1f} vs {rango[0]}"
    col.metric(label=label, value=val_str, delta=delta_str)

st.markdown("---")

# ── Gráfica 1: Población ocupada vs desocupada (área apilada) ─────────────────
st.markdown("### 👥 Población ocupada vs desocupada")
st.caption("Área apilada — misma unidad (personas). Se aprecia cómo crece la fuerza laboral total y qué parte queda desocupada.")

df_pob = df_f[['año', 'pob_ocupada', 'pob_desocupada']].melt(
    id_vars='año', var_name='Estado', value_name='Personas'
)
df_pob['Estado'] = df_pob['Estado'].replace({
    'pob_ocupada':    'Ocupada',
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

# ── Gráfica 2: PIB por trabajador vs Tasa de desempleo (eje doble) ────────────
st.markdown("### 📉 Productividad vs Desempleo")
st.caption(
    "Eje izquierdo = PIB por trabajador (USD). "
    "Eje derecho = Tasa de desempleo (%). "
    "¿Cuando sube la productividad, baja el desempleo?"
)

fig2 = go.Figure()
fig2.add_trace(go.Scatter(
    x=df_f['año'], y=df_f['pib_por_trabajador'],
    mode='lines+markers', name='PIB por Trabajador (USD)',
    line=dict(color="#185FA5", width=2),
    marker=dict(size=5),
    yaxis='y1'
))
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

# ── Gráficas 3 y 4: Correlaciones (2 columnas) ────────────────────────────────
st.markdown("### 🔗 Análisis de correlación")
corr_col1, corr_col2 = st.columns(2, gap="medium")

with corr_col1:
    st.caption("Inflación vs Desempleo — ¿relación de Phillips?")
    fig3 = px.scatter(
        df_f, x='inflacion', y='tasa_desempleo', text='año',
        trendline='ols',
        labels={'inflacion':'Inflación (%)', 'tasa_desempleo': 'Desempleo (%)'},
        color_discrete_sequence=["#378ADD"],
    )
    fig3.update_traces(textposition='top center', marker=dict(size=7))
    fig3.update_layout(height=380, margin=dict(t=20, b=20))
    st.plotly_chart(fig3, use_container_width=True)

with corr_col2:
    st.caption("Ingreso per Cápita vs Desigualdad (Gini)")
    fig4 = px.scatter(
        df_f, x='ingreso_per_capita_ppp', y='indice_gini', text='año',
        trendline='ols',
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

# ── Tabla opcional ─────────────────────────────────────────────────────────────
with st.expander("🗃️ Ver datos del período"):
    cols_show = ['año', 'pob_ocupada','pob_desocupada','poblacion_total',
                 'pib_por_trabajador','tasa_desempleo','inflacion', 'indice_gini',
                 'ingreso_per_capita_ppp']
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
    csv = df_f[cols_show].rename(columns=rename).to_csv(index=False).encode('utf-8')
    st.download_button(
        "⬇️ Descargar CSV", data=csv,
        file_name=f"empleo_economia_{rango[0]}_{rango[1]}.csv", mime="text/csv"
    )