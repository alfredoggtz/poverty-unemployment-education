import streamlit as st

def render():
    st.set_page_config(
        page_title="Pobreza · Desempleo · Educación",
        page_icon="📊",
        layout="wide"
    )

    # ── Header ────────────────────────────────────────────────────────────────
    st.markdown("""
        <h1 style='text-align:center; font-size:2.6rem; margin-bottom:0.2rem;'>
            📊 Pobreza · Desempleo · Educación
        </h1>
        <p style='text-align:center; color:#888; font-size:1.05rem; margin-bottom:2rem;'>
            Análisis de indicadores socioeconómicos de México · 2005–2025
        </p>
        <hr style='border:1px solid #333; margin-bottom:2rem;'>
    """, unsafe_allow_html=True)

    # ── Objetivo ──────────────────────────────────────────────────────────────
    with st.container():
        col_txt, col_metrics = st.columns([2, 1], gap="large")

        with col_txt:
            st.markdown("### 🎯 Objetivo del Proyecto")
            st.markdown("""
Este proyecto surge de una pregunta fundamental:
**¿qué tan relacionados están la educación, el empleo y la economía con los niveles de pobreza en México?**

A través de la recopilación automatizada de datos provenientes del **INEGI** y el **Banco Mundial**,
construimos una base de datos histórica que abarca el período **2005–2025**, integrando indicadores como:

- Índice de Gini e ingreso per cápita
- Tasa de alfabetización y años promedio de escolaridad
- Desempleo y actividad laboral
- Gasto en educación y salud

El objetivo no es solo almacenar cifras, sino **transformar datos dispersos en conocimiento útil**:
identificar patrones, visualizar tendencias y generar evidencia que pueda orientar
la toma de decisiones en materia de política social y económica.
            """)

        with col_metrics:
            st.markdown("### 📌 En números")
            st.metric("Años cubiertos", "2005 – 2025")
            st.metric("Indicadores analizados", "14")
            st.metric("Fuentes de datos", "INEGI + Banco Mundial")
            st.metric("Tablas en la base de datos", "4")

    st.markdown("<hr style='border:1px solid #333; margin: 2rem 0;'>", unsafe_allow_html=True)

    # ── Tarjetas de navegación ────────────────────────────────────────────────
    st.markdown("### 🗺️ Explorar el Dashboard")
    st.markdown("Selecciona una sección para comenzar el análisis:")

    cards = [
        {
            "icon": "📈",
            "title": "Tendencias Globales",
            "desc": "Evolución de la pobreza, desempleo, índice Gini e ingreso per cápita a lo largo del tiempo. Incluye comparación normalizada entre indicadores.",
            "page": "pages/1_📈_Tendencias.py",
            "color": "#1a4a7a",
        },
        {
            "icon": "💼",
            "title": "Empleo & Economía",
            "desc": "Población ocupada vs desocupada, PIB por trabajador, tasa de actividad laboral y correlaciones entre inflación, desempleo y desigualdad.",
            "page": "pages/2_💼_Empleo_Economia.py",
            "color": "#4a1a1a",
        },
        {
            "icon": "🎓",
            "title": "Educación & Gasto Social",
            "desc": "Años de escolaridad, tasa de alfabetización, gasto en educación y salud como porcentaje del PIB, y su relación con la pobreza y el desempleo.",
            "page": "pages/3_🎓_Educacion_Gasto.py",
            "color": "#1a4a2a",
        },
    ]

    cols = st.columns(3, gap="medium")
    for col, card in zip(cols, cards):
        with col:
            st.markdown(f"""
                <div style='
                    background: {card["color"]}22;
                    border: 1px solid {card["color"]}88;
                    border-radius: 12px;
                    padding: 1.5rem;
                    height: 100%;
                '>
                    <div style='font-size:2.2rem; margin-bottom:0.5rem;'>{card["icon"]}</div>
                    <h3 style='margin-bottom:0.6rem; font-size:1.1rem;'>{card["title"]}</h3>
                    <p style='color:#aaa; font-size:0.9rem; line-height:1.5;'>{card["desc"]}</p>
                </div>
            """, unsafe_allow_html=True)
            st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
            st.page_link(card["page"], label=f"Ir a {card['title']} →", use_container_width=True)

    st.markdown("<hr style='border:1px solid #333; margin: 2rem 0;'>", unsafe_allow_html=True)

    # ── Fuentes ───────────────────────────────────────────────────────────────
    st.markdown("### 🔗 Fuentes de Datos")
    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown("""
**INEGI** — Instituto Nacional de Estadística y Geografía
- Población ocupada y desocupada
- [inegi.org.mx](https://www.inegi.org.mx)
        """)
    with c2:
        st.markdown("""
**Banco Mundial** — World Bank Open Data
- Índice Gini, ingreso per cápita, alfabetización, escolaridad,
  desempleo, PIB por trabajador, inflación, gasto social y pobreza
- [data.worldbank.org](https://data.worldbank.org)
        """)

    # ── Footer ────────────────────────────────────────────────────────────────
    st.markdown("""
        <div style='text-align:center; color:#555; font-size:0.8rem; margin-top:2rem;'>
            Proyecto académico · Universidad Autónoma de Baja California (UABC)<br>
            Galvan · García · Severiano · Valle
        </div>
    """, unsafe_allow_html=True)


render()