"""Página «Educación & Gasto Social» del tablero de indicadores socioeconómicos.

Este módulo define una de las páginas de la aplicación multipágina de Streamlit.
Se centra en la educación (escolaridad, alfabetización) y el gasto social
(educación y salud como porcentaje del PIB), así como su relación con la pobreza
y el desempleo, dentro del rango de años seleccionado por el usuario en los
filtros de la barra lateral.

La página se renderiza de arriba hacia abajo en el siguiente orden:

    1. Encabezado con el período y el número de años analizados.
    2. Fila de cuatro métricas resumen (escolaridad, alfabetización, gasto en
       educación y gasto en salud), con su variación respecto al primer año.
    3. Serie temporal de inflación, gasto en educación y gasto en salud sobre un
       mismo eje porcentual (rangos comparables).
    4. Serie temporal de años de escolaridad y alfabetización con doble eje Y.
    5. Gráfica de barras agrupadas que compara gasto en educación vs. salud.
    6. Dos diagramas de dispersión lado a lado: escolaridad vs. pobreza y gasto
       en educación vs. desempleo (con tamaño de punto = gasto en salud), ambos
       con línea de tendencia OLS.
    7. Tabla expandible con los datos del período y botón de descarga a CSV.

Dependencias del proyecto:
    data.loader.load_data: Devuelve el ``DataFrame`` con los indicadores. Debe
        incluir, como mínimo, las columnas usadas en este módulo (``año``,
        ``anos_escolaridad_esp``, ``tasa_alfabetizacion``, ``gasto_educacion``,
        ``gasto_salud``, ``inflacion``, ``tasa_pobreza`` y ``tasa_desempleo``).
    components.filters.render_filters: Dibuja los controles de filtrado y fija
        el rango de años en ``st.session_state``.

Dependencias de terceros:
    streamlit, plotly. Las líneas de tendencia OLS (``trendline='ols'``)
    requieren además el paquete ``statsmodels`` instalado en el entorno.

Estado de sesión (st.session_state):
    rango (tuple[int, int]): Año inicial y final seleccionados en los filtros.
        Si la clave no existe, se usa el rango completo del ``DataFrame``.

Ejemplo de uso:
    Esta página no se ejecuta de forma aislada; Streamlit la carga
    automáticamente desde el directorio ``pages/`` al correr la app::

        streamlit run Inicio.py
"""

import sys, os

# Permite importar los paquetes del proyecto (``data``, ``components``) cuando la
# página se ejecuta desde el subdirectorio ``pages/``: se agrega el directorio
# raíz del proyecto al ``sys.path``.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from data.loader import load_data
from components.filters import render_filters

# Configuración de la página. Debe ser la primera llamada a Streamlit del script.
st.set_page_config(page_title="Educación & Gasto Social", layout="wide")

# Carga del conjunto de datos y renderizado de los filtros de la barra lateral.
df = load_data()
render_filters(df)

# Rango de años activo. Si los filtros aún no lo han fijado en la sesión, se
# toma por defecto el período completo disponible en los datos.
rango = st.session_state.get("rango", (int(df['año'].min()), int(df['año'].max())))

# ── Encabezado ────────────────────────────────────────────────────────────────
st.markdown("## 🎓 Educación & Gasto Social")
st.markdown(f"Período: **{rango[0]} – {rango[1]}** · {rango[1] - rango[0] + 1} años")
st.markdown("---")

# Subconjunto de datos restringido al rango seleccionado. Se copia para evitar
# advertencias de Pandas al asignar sobre una vista.
df_f = df[(df['año'] >= rango[0]) & (df['año'] <= rango[1])].copy()

# ── Métricas rápidas ──────────────────────────────────────────────────────────
st.markdown("### 📌 Resumen del período")

# Cada tupla describe una métrica: (etiqueta visible, columna, unidad a mostrar).
metrics = [
    ("Años de Escolaridad","anos_escolaridad_esp", "años"),
    ("Alfabetización","tasa_alfabetizacion", "%"),
    ("Gasto en Educación","gasto_educacion", "% PIB"),
    ("Gasto en Salud","gasto_salud","% PIB"),
]

# Una columna por métrica. El delta compara el último valor del período contra
# el primero; todos los valores se muestran con dos decimales.
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
# Las tres series están en porcentaje y comparten rangos similares (~3–8%), por
# lo que se grafican sobre un único eje Y para compararlas directamente.
st.markdown("### 📊 Inflación y gasto social (% del PIB / %)")
st.caption(
    "Las tres variables están en porcentaje y tienen rangos similares (3–8%). "
    "Un solo eje Y permite compararlas directamente."
)

fig1 = go.Figure()
# Cada tupla define una serie: (columna, nombre en la leyenda, color de línea).
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
# Años de escolaridad y porcentaje de alfabetización tienen unidades distintas,
# por lo que se usan dos ejes Y independientes (``y1`` izquierdo, ``y2`` derecho).
st.markdown("### 📚 Escolaridad y alfabetización")
st.caption(
    "Eje izquierdo = Años de escolaridad (12–15 años). "
    "Eje derecho = Tasa de alfabetización (91–96%). "
    "Unidades diferentes — cada una con su escala."
)

fig2 = go.Figure()
# Serie sobre el eje izquierdo (y1): años de escolaridad.
fig2.add_trace(go.Scatter(
    x=df_f['año'], y=df_f['anos_escolaridad_esp'],
    mode='lines+markers', name='Años de Escolaridad',
    line=dict(color="#BA7517", width=2),
    marker=dict(size=5),
    yaxis='y1'
))
# Serie sobre el eje derecho (y2): tasa de alfabetización (línea discontinua).
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
# Barras agrupadas por año que permiten comparar, año a año, cuánto del PIB se
# destina a cada rubro de gasto social.
st.markdown("### 💰 Gasto en Educación vs Salud (% del PIB)")
st.caption("Barras agrupadas por año — fácil comparar cuánto se destina a cada rubro.")

# ``melt`` pasa las columnas a formato largo (una fila por año y tipo de gasto)
# para que Plotly Express pueda agrupar las barras por la categoría ``Tipo``.
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

# ── Gráficas 4 y 5: Correlaciones (2 columnas) ────────────────────────────────
# Dos diagramas de dispersión colocados lado a lado, cada uno con su línea de
# tendencia OLS y los puntos etiquetados por año.
st.markdown("### 🔗 Análisis de correlación")
corr_col1, corr_col2 = st.columns(2, gap="medium")

with corr_col1:
    # Relación escolaridad–pobreza.
    st.caption("Años de escolaridad vs Pobreza — ¿más educación, menos pobreza?")
    fig4 = px.scatter(
        df_f, x='anos_escolaridad_esp', y='tasa_pobreza', text='año',
        trendline='ols',  # Requiere statsmodels.
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
    # Relación gasto en educación–desempleo. El tamaño de cada punto codifica una
    # tercera variable: el gasto en salud (``size='gasto_salud'``).
    st.caption("Gasto en educación vs Desempleo (tamaño = gasto en salud)")
    fig5 = px.scatter(
        df_f, x='gasto_educacion', y='tasa_desempleo', text='año',
        size='gasto_salud',
        trendline='ols',  # Requiere statsmodels.
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

# ── Tabla opcional ─────────────────────────────────────────────────────────────
# Sección colapsable con los datos crudos del período y opción de descarga.
with st.expander("🗃️ Ver datos del período"):
    # Columnas a mostrar y su renombrado para una presentación legible.
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
    # Exporta la misma vista a CSV (codificado en UTF-8) para la descarga.
    csv = df_f[cols_show].rename(columns=rename).to_csv(index=False).encode('utf-8')
    st.download_button(
        "⬇️ Descargar CSV", data=csv,
        file_name=f"educacion_gasto_{rango[0]}_{rango[1]}.csv", mime="text/csv"
    )