import streamlit as st
from PIL import Image
from services.image_processor import ImageProcessor
from web.styles import inject_styles
from web.components.header import render_header
from web.components.sidebar import render_sidebar, render_action_button
from web.components.image_preview import render_original, render_result, render_empty_state
from web.components.loader import GenericLoader

st.set_page_config(page_title="File Converter", layout="wide")

inject_styles()
render_header()

action, target_format = render_sidebar()

uploaded_file = st.file_uploader(
    "Carica un'immagine",
    type=["png", "jpg", "jpeg", "webp", "bmp"],
    label_visibility="collapsed",
)

if uploaded_file is None:
    render_empty_state()
    st.stop()

try:
    image = Image.open(uploaded_file)
except Exception as e:
    st.error(f"Errore nel caricamento del file: {e}")
    st.stop()

col1, col2 = st.columns(2, gap="large")
render_original(col1, image, uploaded_file.name)

if not render_action_button(action, target_format):
    st.stop()

loader = GenericLoader("Elaborazione in corso...", "Analisi dell'immagine...")

try:
    if action == "Converti Formato":
        loader.update(subtext=f"Conversione in {target_format}...")
        result_image = ImageProcessor.convert_format(image, target_format)
    else:
        loader.update(subtext="Rimozione dello sfondo...")
        result_image = ImageProcessor.remove_background(image)
        target_format = "PNG"

    loader.update("Ottimizzazione...", "Quasi finito!")

    loader.success()
    render_result(col2, result_image, target_format)

except Exception as e:
    loader.success()
    st.error(f"Errore durante l'elaborazione: {e}")
