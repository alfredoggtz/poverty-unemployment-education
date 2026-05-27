import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from data.loader import load_data
from components.filters import render_filters

st.set_page_config(page_title="Educación & Gasto Social", layout="wide")

df = load_data()
render_filters(df)
rango = st.session_state.get("rango", (int(df['año'].min()), int(df['año'].max())))

st.markdown("## 🎓 Educación & Gasto Social")
st.markdown(f"Período: **{rango[0]} – {rango[1]}** · {rango[1] - rango[0] + 1} años")
st.markdown("---")

df_f = df[(df['año'] >= rango[0]) & (df['año'] <= rango[1])].copy()

# ── Métricas rápidas ──────────────────────────────────────────────────────────
st.markdown("### 📌 Resumen del período")

metrics = [
    ("Años de Escolaridad","anos_escolaridad_esp", "años"),
    ("Alfabetización","tasa_alfabetizacion",  "%"),
    ("Gasto en Educación","gasto_educacion",      "% PIB"),
    ("Gasto en Salud","gasto_salud","% PIB"),
]

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

# ── Gráfica 1: Inflación · Gasto educación · Gasto salud (mismo eje %) ────────
st.markdown("### 📊 Inflación y gasto social (% del PIB / %)")
st.caption(
    "Las tres variables están en porcentaje y tienen rangos similares (3–8%). "
    "Un solo eje Y permite compararlas directamente."
)

fig1 = go.Figure()
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

# ── Gráfica 2: Escolaridad vs Alfabetización (eje doble) ─────────────────────
st.markdown("### 📚 Escolaridad y alfabetización")
st.caption(
    "Eje izquierdo = Años de escolaridad (12–15 años). "
    "Eje derecho = Tasa de alfabetización (91–96%). "
    "Unidades diferentes — cada una con su escala."
)

fig2 = go.Figure()
fig2.add_trace(go.Scatter(
    x=df_f['año'], y=df_f['anos_escolaridad_esp'],
    mode='lines+markers', name='Años de Escolaridad',
    line=dict(color="#BA7517", width=2),
    marker=dict(size=5),
    yaxis='y1'
))
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

# ── Gráfica 3: Gasto educación vs salud (barras agrupadas) ───────────────────
st.markdown("### 💰 Gasto en Educación vs Salud (% del PIB)")
st.caption("Barras agrupadas por año — fácil comparar cuánto se destina a cada rubro.")

df_gasto = df_f[['año', 'gasto_educacion', 'gasto_salud']].melt(
    id_vars='año', var_name='Tipo', value_name='% del PIB'
)
df_gasto['Tipo'] = df_gasto['Tipo'].replace({
    'gasto_educacion': 'Educación',
    'gasto_salud':     'Salud',
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

# ── Gráficas 4 y 5: Correlaciones (2 columnas) ────────────────────────────────
st.markdown("### 🔗 Análisis de correlación")
corr_col1, corr_col2 = st.columns(2, gap="medium")

with corr_col1:
    st.caption("Años de escolaridad vs Pobreza — ¿más educación, menos pobreza?")
    fig4 = px.scatter(
        df_f, x='anos_escolaridad_esp', y='tasa_pobreza', text='año',
        trendline='ols',
        labels={
            'anos_escolaridad_esp': 'Años de Escolaridad',
            'tasa_pobreza':         'Pobreza (%)',
        },
        color_discrete_sequence=["#BA7517"],
    )
    fig4.update_traces(textposition='top center', marker=dict(size=7))
    fig4.update_layout(height=380, margin=dict(t=20, b=20))
    st.plotly_chart(fig4, use_container_width=True)

with corr_col2:
    st.caption("Gasto en educación vs Desempleo (tamaño = gasto en salud)")
    fig5 = px.scatter(
        df_f, x='gasto_educacion', y='tasa_desempleo', text='año',
        size='gasto_salud',
        trendline='ols',
        labels={
            'gasto_educacion': 'Gasto Educación (% PIB)',
            'tasa_desempleo':  'Desempleo (%)',
        },
        color_discrete_sequence=["#1D9E75"],
    )
    fig5.update_traces(textposition='top center')
    fig5.update_layout(height=380, margin=dict(t=20, b=20))
    st.plotly_chart(fig5, use_container_width=True)

st.markdown("---")

# ── Tabla opcional ─────────────────────────────────────────────────────────────
with st.expander("🗃️ Ver datos del período"):
    cols_show = ['año', 'anos_escolaridad_esp', 'tasa_alfabetizacion',
                 'gasto_educacion', 'gasto_salud', 'inflacion',
                 'tasa_pobreza', 'tasa_desempleo']
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
    csv = df_f[cols_show].rename(columns=rename).to_csv(index=False).encode('utf-8')
    st.download_button(
        "⬇️ Descargar CSV", data=csv,
        file_name=f"educacion_gasto_{rango[0]}_{rango[1]}.csv", mime="text/csv"
    )