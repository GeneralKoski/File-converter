import streamlit as st
import io


def render_original(col, image, filename):
    with col:
        st.markdown("<h4>Originale</h4>", unsafe_allow_html=True)
        st.image(image, use_container_width=True)
        st.caption(filename)


def render_result(col, result_image, target_format):
    with col:
        st.markdown("<h4>Risultato</h4>", unsafe_allow_html=True)
        st.image(result_image, use_container_width=True)

        data, file_ext = _prepare_download(result_image, target_format)

        st.download_button(
            label="Scarica Immagine",
            data=data,
            file_name=f"processed_image.{file_ext}",
            mime=f"image/{file_ext}",
            use_container_width=True,
        )


def render_empty_state():
    st.markdown(
        "<div style='text-align:center; padding: 4rem 0; color: #999;'>"
        "<p style='font-size: 1.1rem;'>Carica un'immagine per iniziare</p>"
        "</div>",
        unsafe_allow_html=True,
    )


def _prepare_download(image, target_format):
    buf = io.BytesIO()
    save_format = target_format.upper()
    if save_format == "JPG":
        save_format = "JPEG"

    img = image
    if save_format == "JPEG" and img.mode == "RGBA":
        img = img.convert("RGB")

    img.save(buf, format=save_format)
    return buf.getvalue(), target_format.lower()
