import streamlit as st

ACTIONS = ["Converti Formato", "Rimuovi Sfondo"]
FORMATS = ["PNG", "JPG", "WEBP"]


def render_sidebar():
    st.sidebar.markdown(
        "<h3 style='margin-bottom: 1rem;'>Impostazioni</h3>",
        unsafe_allow_html=True,
    )
    action = st.sidebar.radio("Operazione", ACTIONS, label_visibility="collapsed")

    target_format = "PNG"
    if action == "Converti Formato":
        target_format = st.sidebar.selectbox("Formato di Output", FORMATS)

    st.sidebar.markdown("---")

    return action, target_format


def render_action_button(action, target_format):
    if action == "Converti Formato":
        return st.sidebar.button(
            f"Converti in {target_format}",
            type="primary",
            use_container_width=True,
        )
    return st.sidebar.button(
        "Rimuovi Sfondo",
        type="primary",
        use_container_width=True,
    )
