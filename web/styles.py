STYLESHEET = """
<style>
    /* Remove anchor links on headers */
    h1 a, h2 a, h3 a, h4 a, h5 a, h6 a,
    .stMarkdown a[href^="#"] {
        display: none !important;
    }

    [data-testid="stHeaderActionElements"] {
        display: none !important;
    }

    .stMarkdown a {
        pointer-events: none;
        text-decoration: none !important;
        color: inherit !important;
    }

    /* Main container */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #fafafa;
    }

    [data-testid="stSidebar"] .block-container {
        padding-top: 2rem;
    }

    /* Image containers */
    [data-testid="stImage"] {
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid #e0e0e0;
    }

    /* Download button */
    .stDownloadButton > button {
        width: 100%;
    }

    /* Divider */
    hr {
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-color: #e8e8e8;
    }
</style>
"""


def inject_styles():
    import streamlit as st
    st.markdown(STYLESHEET, unsafe_allow_html=True)
