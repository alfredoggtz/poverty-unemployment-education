"""Página «Tendencias Globales» del tablero de indicadores socioeconómicos.

Este módulo define una de las páginas de la aplicación multipágina de Streamlit.
Presenta la evolución temporal de los principales indicadores socioeconómicos
(pobreza, desempleo, desigualdad e ingreso) dentro del rango de años que el
usuario selecciona mediante los filtros de la barra lateral.

La página se renderiza de arriba hacia abajo en el siguiente orden:

    1. Encabezado con el período y el número de años analizados.
    2. Fila de cuatro métricas resumen, cada una con su variación (delta)
       respecto al primer año del período.
    3. Serie temporal de pobreza, desempleo y actividad laboral, todas sobre
       un mismo eje porcentual para permitir comparación directa.
    4. Diagrama de dispersión Gini vs. pobreza con línea de tendencia OLS.
    5. Serie temporal de ingreso per cápita y PIB por trabajador con doble eje
       Y (distintas magnitudes, cada una con su propia escala).
    6. Tabla expandible con los datos del período y botón de descarga a CSV.

Dependencias del proyecto:
    data.loader.load_data: Devuelve el ``DataFrame`` con los indicadores. Debe
        incluir, como mínimo, las columnas usadas en este módulo (``año``,
        ``tasa_pobreza``, ``tasa_desempleo``, ``tasa_actividad_laboral``,
        ``indice_gini``, ``ingreso_per_capita_ppp`` y ``pib_por_trabajador``).
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
st.set_page_config(page_title="Tendencias Globales", layout="wide")

# Carga del conjunto de datos y renderizado de los filtros de la barra lateral.
df = load_data()
render_filters(df)

# Rango de años activo. Si los filtros aún no lo han fijado en la sesión, se
# toma por defecto el período completo disponible en los datos.
rango = st.session_state.get("rango", (int(df['año'].min()), int(df['año'].max())))

# ── Encabezado ────────────────────────────────────────────────────────────────
st.markdown("## 📈 Tendencias Globales")
st.markdown(f"Período: **{rango[0]} – {rango[1]}** · {rango[1] - rango[0] + 1} años")
st.markdown("---")

# Subconjunto de datos restringido al rango seleccionado. Se copia para evitar
# advertencias de Pandas al asignar sobre una vista.
df_f = df[(df['año'] >= rango[0]) & (df['año'] <= rango[1])].copy()

# ── Métricas rápidas ──────────────────────────────────────────────────────────
st.markdown("### 📌 Resumen del período")

# Cada tupla describe una métrica: (etiqueta visible, columna, unidad a mostrar).
metrics = [
    ("Tasa de Pobreza", "tasa_pobreza", "%"),
    ("Tasa de Desempleo", "tasa_desempleo", "%"),
    ("Índice de Gini", "indice_gini", ""),
    ("Ingreso per Cápita", "ingreso_per_capita_ppp", "USD"),
]

# Una columna por métrica. El delta compara el último valor del período contra
# el primero (``iloc[-1]`` vs. ``iloc[0]``), por lo que el ``DataFrame`` debe
# venir ordenado cronológicamente.
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

# ── Gráfica 1: Pobreza · Desempleo · Actividad laboral (mismo eje %) ──────────
# Las tres series comparten unidad (porcentaje), de modo que se grafican sobre
# un único eje Y para facilitar la comparación visual directa.
st.markdown("### 📊 Pobreza, desempleo y actividad laboral")
st.caption("Las tres variables están en porcentaje — comparación directa en el mismo eje.")

fig1 = go.Figure()
# Cada tupla define una serie: (columna, nombre en la leyenda, color de línea).
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

# ── Gráfica 2: Gini vs Pobreza (scatter por año) ──────────────────────────────
# Diagrama de dispersión donde cada punto es un año. La línea de tendencia OLS
# ayuda a visualizar la relación entre desigualdad y pobreza.
st.markdown("### 🔵 Desigualdad vs Pobreza")
st.caption("Cada punto es un año. ¿A mayor desigualdad (Gini), mayor pobreza?")

fig2 = px.scatter(
    df_f,
    x='indice_gini', y='tasa_pobreza',
    text='año',                # Etiqueta cada punto con su año.
    trendline='ols',           # Regresión lineal por mínimos cuadrados (requiere statsmodels).
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

# ── Gráfica 3: Ingreso per cápita vs PIB por trabajador (eje doble) ───────────
# Ambas series usan dólares pero en órdenes de magnitud distintos, por lo que se
# emplean dos ejes Y independientes (``y1`` izquierdo, ``y2`` derecho).
st.markdown("### 💰 Ingreso per cápita y productividad")
st.caption(
    "Eje izquierdo = Ingreso per cápita PPP (USD · escala 13k–26k). "
    "Eje derecho = PIB por trabajador (USD · escala 48k–53k). "
    "Distintas magnitudes — cada una con su propia escala."
)

fig3 = go.Figure()
# Serie sobre el eje izquierdo (y1): ingreso per cápita.
fig3.add_trace(go.Scatter(
    x=df_f['año'], y=df_f['ingreso_per_capita_ppp'],
    mode='lines+markers', name='Ingreso per Cápita PPP (USD)',
    line=dict(color="#BA7517", width=2),
    marker=dict(size=5),
    yaxis='y1'
))
# Serie sobre el eje derecho (y2): PIB por trabajador (línea discontinua para
# distinguirla visualmente del primer eje).
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
    # ``overlaying='y'`` superpone el segundo eje sobre el primero; ``side='right'``
    # lo coloca a la derecha.
    yaxis2=dict(title="PIB por Trabajador (USD)", overlaying='y', side='right', tickformat=","),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    margin=dict(t=40, b=40)
)
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# ── Tabla opcional ─────────────────────────────────────────────────────────────
# Sección colapsable con los datos crudos del período y opción de descarga.
with st.expander("🗃️ Ver datos del período"):
    # Columnas a mostrar y su renombrado para una presentación legible.
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
    # Exporta la misma vista a CSV (codificado en UTF-8) para la descarga.
    csv = df_f[cols_show].rename(columns=rename).to_csv(index=False).encode('utf-8')
    st.download_button(
        "⬇️ Descargar CSV", data=csv,
        file_name=f"tendencias_{rango[0]}_{rango[1]}.csv", mime="text/csv"
    )