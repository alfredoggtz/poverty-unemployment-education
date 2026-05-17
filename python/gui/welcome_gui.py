import streamlit as st

def render():
    st.set_page_config(
        page_title="Welcome to Poverty-Unemployment-Education",
        layout="centered"
    )

    st.title("Bienvenido al Proyecto Pobreza-Desempleo-Educación")
    st.markdown("""
    **Objetivo:** Este proyecto surge de una pregunta fundamental: ¿qué tan relacionados están la educación, el empleo y la economía con los niveles de pobreza en México?\n\n
A través de la recopilación automatizada de datos provenientes del INEGI y el Banco Mundial, construimos una base de datos histórica que abarca el período 2005–2025, integrando indicadores como el índice Gini, el ingreso per cápita, la tasa de alfabetización, los años promedio de escolaridad y el desempleo.\n
El objetivo no es solo almacenar cifras, sino transformar datos dispersos en conocimiento útil: identificar patrones, visualizar tendencias y generar evidencia que pueda orientar la toma de decisiones en materia de política social y económica.\n
Este panel interactivo representa la capa de visualización del sistema: un espacio donde los indicadores cobran forma, donde los años se pueden comparar y donde las correlaciones entre variables dejan de ser abstractas para volverse visibles.
    """)

render()