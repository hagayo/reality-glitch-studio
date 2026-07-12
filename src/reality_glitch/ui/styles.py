import streamlit as st


def apply_styles() -> None:
    st.markdown(
        """
        <style>
            .stApp { direction: rtl; }
            .block-container { max-width: 1350px; padding-top: 1.8rem; }
            h1, h2, h3, p, label { text-align: right; }
            div[data-testid="stImage"] img { border-radius: 18px; }
            .hero, .pipeline-box {
                padding: 1rem 1.2rem;
                border: 1px solid rgba(128,128,128,.25);
                border-radius: 16px;
                margin-bottom: 1rem;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
