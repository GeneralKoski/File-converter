import streamlit as st


def render_header():
    st.markdown(
        "<h1 style='margin-bottom: 0.2rem;'>Image Converter & Background Remover</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='color: #666; margin-bottom: 2rem;'>Converti le tue immagini o rimuovi lo sfondo</p>",
        unsafe_allow_html=True,
    )
