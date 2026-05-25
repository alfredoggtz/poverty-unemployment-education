import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import plotly.express as px

from data.loader import load_data
from components.filters import render_filters

# Configuración
st.set_page_config(page_title="Empleo & Economía", layout="wide")

# ── Indicadores disponibles
INDICADORES = {
    "Población Ocupada": "pob_ocupada",
    "Población Desocupada": "pob_desocupada",
    "Población Total": "poblacion_total",
    "PIB por Trabajador (USD)": "pib_por_trabajador",
    "Tasa de Actividad Laboral (%)": "tasa_actividad_laboral",
    "Tasa de Desempleo (%)": "tasa_desempleo",
    "Inflación (%)": "inflacion",
    "Índice de Gini": "indice_gini",
    "Ingreso per Cápita PPP (USD)": "ingreso_per_capita_ppp",
    "Tasa de Pobreza (%)": "tasa_pobreza",
}

CHART_TYPES = ["Línea", "Barra", "Área"]

# Carga de datos y filtro global de año (sidebar)
df = load_data()
render_filters(df)
rango = st.session_state.get("rango", (int(df['año'].min()), int(df['año'].max())))

# Header
st.markdown("## 💼 Empleo & Economía")
st.markdown("---")

# Filtros locales en la parte superior
with st.container():
    st.markdown("### 🎛️ Filtros")
    col_a, col_b, col_c = st.columns([3, 1.2, 0.8], gap="medium")

    with col_a:
        indicadores_sel = st.multiselect(
            "Indicadores",
            options=list(INDICADORES.keys()),
            default=["Población Ocupada", "Población Desocupada", "PIB por Trabajador (USD)", "Tasa de Actividad Laboral (%)"]
        )

    with col_b:
        chart_type = st.radio("Tipo de gráfica", CHART_TYPES, horizontal=False)

    with col_c:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        mostrar_tabla = st.checkbox("Mostrar tabla", value=False)

st.markdown("---")

# Filtrar datos
df_f = df[(df['año'] >= rango[0]) & (df['año'] <= rango[1])].copy()
st.markdown(f"Período seleccionado: **{rango[0]} – {rango[1]}** · {rango[1] - rango[0] + 1} años")
st.markdown("---")

# Validación
if not indicadores_sel:
    st.warning("Selecciona al menos un indicador en los filtros de arriba.")
    st.stop()

# Métricas rápidas
st.markdown("### 📌 Promedios del período")
cols_met = st.columns(min(len(indicadores_sel), 4))
for i, nombre in enumerate(indicadores_sel[:4]):
    col_id = INDICADORES[nombre]
    val    = df_f[col_id].mean()
    delta  = df_f[col_id].iloc[-1] - df_f[col_id].iloc[0]
    cols_met[i].metric(
        label=nombre,
        value=f"{val:,.2f}",
        delta=f"{delta:+.2f} vs {rango[0]}"
    )

st.markdown("---")

# Gráfica principal
st.markdown("### 📊 Evolución de indicadores seleccionados")

# Separar indicadores de población (escala grande) de los porcentuales
POBLACION = {"pob_ocupada", "pob_desocupada", "poblacion_total"}
cols_sel  = [INDICADORES[n] for n in indicadores_sel]
es_pob    = all(c in POBLACION for c in cols_sel)
es_mix    = any(c in POBLACION for c in cols_sel) and any(c not in POBLACION for c in cols_sel)

if es_mix:
    st.info("ℹ️ Mezcla de indicadores de población (valores grandes) con porcentuales — se muestran normalizados (0–1) para comparar en la misma escala.")

if len(indicadores_sel) == 1:
    col_id = INDICADORES[indicadores_sel[0]]
    if chart_type == "Línea":
        fig = px.line(df_f, x='año', y=col_id, markers=True,
                      labels={col_id: indicadores_sel[0], 'año': 'Año'}, title=indicadores_sel[0])
    elif chart_type == "Barra":
        fig = px.bar(df_f, x='año', y=col_id,
                     labels={col_id: indicadores_sel[0], 'año': 'Año'}, title=indicadores_sel[0])
    else:
        fig = px.area(df_f, x='año', y=col_id,
                      labels={col_id: indicadores_sel[0], 'año': 'Año'}, title=indicadores_sel[0])
    fig.update_layout(height=420)
    st.plotly_chart(fig, use_container_width=True)

else:
    nombre_map = {INDICADORES[n]: n for n in indicadores_sel}
    df_norm = df_f[['año'] + cols_sel].copy()
    for col in cols_sel:
        mn, mx = df_norm[col].min(), df_norm[col].max()
        df_norm[col] = (df_norm[col] - mn) / (mx - mn) if mx != mn else 0
    df_norm = df_norm.rename(columns=nombre_map)
    df_melted = df_norm.melt(id_vars='año', var_name='Indicador', value_name='Valor normalizado (0–1)')

    if chart_type == "Línea":
        fig = px.line(df_melted, x='año', y='Valor normalizado (0–1)',
                      color='Indicador', markers=True,
                      title="Evolución comparada (normalizado 0–1)")
    elif chart_type == "Barra":
        fig = px.bar(df_melted, x='año', y='Valor normalizado (0–1)',
                     color='Indicador', barmode='group',
                     title="Evolución comparada (normalizado 0–1)")
    else:
        fig = px.area(df_melted, x='año', y='Valor normalizado (0–1)',
                      color='Indicador',
                      title="Evolución comparada (normalizado 0–1)")
    fig.update_layout(height=450)
    st.plotly_chart(fig, use_container_width=True)
    st.caption("ℹ️ Valores normalizados entre 0 y 1 para comparar indicadores con distintas unidades.")

st.markdown("---")

# Gráficas individuales
if len(indicadores_sel) > 1:
    st.markdown("### 🔍 Detalle por indicador")
    for i in range(0, len(indicadores_sel), 2):
        par = indicadores_sel[i:i+2]
        cols = st.columns(len(par), gap="medium")
        for col_ui, nombre in zip(cols, par):
            col_id = INDICADORES[nombre]
            with col_ui:
                if chart_type == "Línea":
                    fig = px.line(df_f, x='año', y=col_id, markers=True,
                                  labels={col_id: nombre, 'año': 'Año'}, title=nombre)
                elif chart_type == "Barra":
                    fig = px.bar(df_f, x='año', y=col_id,
                                 labels={col_id: nombre, 'año': 'Año'}, title=nombre)
                else:
                    fig = px.area(df_f, x='año', y=col_id,
                                  labels={col_id: nombre, 'año': 'Año'}, title=nombre)
                fig.update_layout(height=320, margin=dict(t=40, b=20))
                st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Análisis de correlación fijo
st.markdown("### 🔗 Análisis de correlación")
corr_col1, corr_col2 = st.columns(2, gap="medium")

with corr_col1:
    fig_c1 = px.scatter(
        df_f, x='inflacion', y='tasa_desempleo', text='año',
        title='Inflación vs Tasa de Desempleo',
        labels={'inflacion': 'Inflación (%)', 'tasa_desempleo': 'Desempleo (%)'},
        trendline='ols'
    )
    fig_c1.update_traces(textposition='top center')
    fig_c1.update_layout(height=380)
    st.plotly_chart(fig_c1, use_container_width=True)

with corr_col2:
    fig_c2 = px.scatter(
        df_f, x='ingreso_per_capita_ppp', y='indice_gini', text='año',
        title='Ingreso per Cápita vs Índice de Gini',
        labels={'ingreso_per_capita_ppp': 'Ingreso per Cápita (USD PPP)', 'indice_gini': 'Índice Gini'},
        trendline='ols'
    )
    fig_c2.update_traces(textposition='top center')
    fig_c2.update_layout(height=380)
    st.plotly_chart(fig_c2, use_container_width=True)

# Tabla de datos
if mostrar_tabla:
    st.markdown("---")
    st.markdown("### 🗃️ Datos del período")
    cols_mostrar = ['año'] + [INDICADORES[n] for n in indicadores_sel]
    rename_map   = {INDICADORES[n]: n for n in indicadores_sel}
    st.dataframe(
        df_f[cols_mostrar].rename(columns=rename_map).set_index('año'),
        use_container_width=True
    )
    csv = df_f[cols_mostrar].rename(columns=rename_map).to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Descargar CSV", data=csv,
                       file_name=f"empleo_economia_{rango[0]}_{rango[1]}.csv", mime="text/csv")