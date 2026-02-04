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
    /* Sidebar */
    /* [data-testid="stSidebar"] {
        background-color: #fafafa;
    } */

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

    /* Custom Loader Overlay */
    .custom-loader-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: rgba(0, 0, 0, 0.7);
        z-index: 999999;
        display: flex;
        justify-content: center;
        align-items: center;
        backdrop-filter: blur(4px);
    }

    .custom-loader-box {
        background: #1e1e1e;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        text-align: center;
        min-width: 320px;
        border: 1px solid #333;
        color: white;
    }

    .custom-loader-spinner {
        border: 3px solid rgba(255,255,255,0.1);
        border-top: 3px solid #ff4b4b; /* Streamlit Red/Pink or user theme color */
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
        margin: 0 auto 1.5rem auto;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    .loader-text {
        font-size: 1.1rem;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }

    .loader-subtext {
        font-size: 0.9rem;
        color: #888;
    }
</style>
"""


def inject_styles():
    import streamlit as st
    st.markdown(STYLESHEET, unsafe_allow_html=True)
