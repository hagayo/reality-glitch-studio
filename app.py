from __future__ import annotations

import random
from io import BytesIO

import streamlit as st
from PIL import Image, UnidentifiedImageError

from effects import (
    enhance_result, glitch_effect, mirror_effect, portal_effect, prepare_image, rgb_split_effect, wave_effect,
)


APP_TITLE = "Reality Glitch Studio" 
EFFECT_WAVE = "גל במציאות" 
EFFECT_GLITCH = "התפרקות דיגיטלית" 
EFFECT_RGB = "הפרדת צבעים" 
EFFECT_MIRROR = "מראה בלתי אפשרית" 
EFFECT_PORTAL = "פורטל אינסופי" 

st.set_page_config( page_title=APP_TITLE, page_icon="🌀", layout="wide", )

def add_custom_style() -> None:
    """ Add a small amount of CSS to improve the visual presentation. """
    st.markdown(
    """ <style>
        .stApp { direction: rtl; }
        .block-container { max-width: 1250px; padding-top: 2rem; padding-bottom: 4rem; }
        h1, h2, h3, p, label { text-align: right; }
        .app-subtitle { font-size: 1.15rem; opacity: 0.82; margin-bottom: 1.8rem; }
        .info-card { padding: 1rem 1.2rem; border: 1px solid rgba(128, 128, 128, 0.25); border-radius: 16px; margin-bottom: 1rem; }
        div[data-testid="stImage"] img { border-radius: 18px; }
        </style>
    """,
    unsafe_allow_html=True,
)        


def image_to_png_bytes(image: Image.Image) -> bytes:
    """ Convert a Pillow image into PNG bytes without saving a temporary file. """
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0) 
    return buffer.getvalue() 


def show_welcome_screen() -> None:
    """ Display instructions before the user uploads an image. """
    st.markdown(
        """
        <div class="info-card">
            <strong>איך מתחילים?</strong><br><br>
            1. מעלים תמונת JPG או PNG.<br>
            2. בוחרים אפקט.<br>
            3. משנים את הפרמטרים.<br> 
            4. מורידים את היצירה החדשה.
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    st.info( "מומלץ לבחור תמונה צבעונית עם אדם, נוף, רחוב או מבנה ברור." )






if __name__ == "__main__":
    main()
