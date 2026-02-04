
import streamlit as st
import time

class GenericLoader:
    def __init__(self, text="Loading...", subtext="Checking files..."):
        self.placeholder = st.empty()
        self.text = text
        self.subtext = subtext
        self._render()

    def update(self, text=None, subtext=None):
        if text:
            self.text = text
        if subtext:
            self.subtext = subtext
        self._render()
        # Small delay to let user see the update if needed, but not strictly necessary for functionality
        # time.sleep(0.5)

    def _render(self):
        self.placeholder.markdown(
            f"""
            <div class="custom-loader-overlay">
                <div class="custom-loader-box">
                    <div class="custom-loader-spinner"></div>
                    <div class="loader-text">{self.text}</div>
                    <div class="loader-subtext">{self.subtext}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    def success(self, text="Done!"):
        self.placeholder.empty()
        # Optionally show a success toast or just disappear
