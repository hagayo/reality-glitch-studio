from __future__ import annotations

import logging
from io import BytesIO

import streamlit as st
from PIL import Image, UnidentifiedImageError

from reality_glitch.container import build_container
from reality_glitch.domain.exceptions import RealityGlitchError
from reality_glitch.domain.models import (
    AnimationOptions,
    EffectId,
    EffectStep,
    FinishSettings,
    PipelineRequest,
)
from reality_glitch.ui.controls import (
    DEFAULT_SETTINGS,
    DISPLAY_NAMES,
    render_effect_settings,
)
from reality_glitch.ui.state import EditorState
from reality_glitch.ui.styles import apply_styles


logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
APP_TITLE = "Reality Glitch Studio - SOLID Edition"
CONTAINER = build_container()

st.set_page_config(page_title=APP_TITLE, page_icon="🌀", layout="wide")


def initialize_state() -> None:
    if "editor" not in st.session_state:
        default_preset = CONTAINER.presets.get("מותאם אישית")
        st.session_state.editor = EditorState.from_preset(default_preset)


def load_preset(name: str) -> None:
    st.session_state.editor = EditorState.from_preset(
        CONTAINER.presets.get(name)
    )


def render_sidebar() -> tuple[object, EditorState]:
    editor: EditorState = st.session_state.editor

    with st.sidebar:
        st.header("1. תמונה")
        uploaded_file = st.file_uploader(
            "העלאת JPG, PNG או WEBP",
            type=["jpg", "jpeg", "png", "webp"],
        )

        st.header("2. Preset")
        preset_names = [preset.name for preset in CONTAINER.presets.list_all()]
        preset_name = st.selectbox(
            "בחירת סגנון מוכן",
            preset_names,
            index=preset_names.index(editor.active_preset),
        )
        if st.button("טען Preset", use_container_width=True):
            load_preset(preset_name)
            st.rerun()

        st.header("3. Pipeline")
        selected_ids = st.multiselect(
            "בחרו אפקטים לפי סדר ההפעלה",
            list(EffectId),
            default=[step.effect_id for step in editor.steps],
            max_selections=4,
            format_func=DISPLAY_NAMES.get,
        )

        existing = {step.effect_id: step for step in editor.steps}
        steps = [
            existing.get(
                effect_id,
                EffectStep(effect_id, dict(DEFAULT_SETTINGS[effect_id])),
            )
            for effect_id in selected_ids
        ]

        if steps:
            st.markdown(
                '<div class="pipeline-box">'
                + " ← ".join(DISPLAY_NAMES[step.effect_id] for step in steps)
                + "</div>",
                unsafe_allow_html=True,
            )

        edited_steps = [
            render_effect_settings(step, index)
            for index, step in enumerate(steps)
        ]

        st.header("4. גימור")
        contrast = st.slider(
            "ניגודיות", 0.5, 2.0, float(editor.finish.contrast), 0.05
        )
        color = st.slider(
            "עוצמת צבע", 0.0, 2.5, float(editor.finish.color), 0.05
        )

        editor.steps = edited_steps
        editor.finish = FinishSettings(contrast, color)
        if preset_name != editor.active_preset:
            editor.active_preset = "מותאם אישית"

    return uploaded_file, editor


def main() -> None:
    initialize_state()
    apply_styles()

    st.title(APP_TITLE)
    st.markdown(
        '<div class="hero">מעלים תמונה, בונים שרשרת אפקטים '
        "ומפיקים PNG או GIF מונפש.</div>",
        unsafe_allow_html=True,
    )

    uploaded_file, editor = render_sidebar()
    if uploaded_file is None:
        st.info("העלו תמונה כדי להתחיל.")
        return
    if not editor.steps:
        st.warning("יש לבחור לפחות אפקט אחד.")
        return

    try:
        original = CONTAINER.image_service.prepare(Image.open(uploaded_file))
        request = PipelineRequest(
            steps=tuple(editor.steps),
            finish=editor.finish,
            include_intermediate_steps=True,
        )
        result = CONTAINER.pipeline.execute(original, request)
    except (RealityGlitchError, UnidentifiedImageError, OSError, ValueError) as error:
        LOGGER.exception("Failed to process image")
        st.error("לא הצלחנו לעבד את התמונה. בדקו שהקובץ וההגדרות תקינים.")
        st.code(str(error))
        return

    source_column, result_column = st.columns(2)
    with source_column:
        st.subheader("מקור")
        st.image(original, use_container_width=True)
    with result_column:
        st.subheader("תוצאה")
        st.image(result.image, use_container_width=True)

    if result.steps:
        st.subheader("שלבי ה-Pipeline")
        columns = st.columns(min(4, len(result.steps)))
        for index, step_result in enumerate(result.steps):
            with columns[index % len(columns)]:
                st.caption(f"{index + 1}. {DISPLAY_NAMES[step_result.effect_id]}")
                st.image(step_result.image, use_container_width=True)

    png_column, gif_column = st.columns(2)
    with png_column:
        st.subheader("PNG")
        st.download_button(
            "הורדת PNG",
            CONTAINER.exporter.to_png(result.image),
            "reality-glitch.png",
            "image/png",
            use_container_width=True,
        )

    with gif_column:
        st.subheader("GIF")
        frame_count = st.slider("מספר פריימים", 5, 24, 12)
        frame_duration = st.slider("משך פריים במילישניות", 50, 300, 90, 10)
        gif_data = CONTAINER.animation.render_gif(
            original,
            PipelineRequest(tuple(editor.steps), editor.finish),
            AnimationOptions(frame_count, frame_duration),
        )
        st.image(gif_data)
        st.download_button(
            "הורדת GIF",
            gif_data,
            "reality-glitch-animation.gif",
            "image/gif",
            use_container_width=True,
        )


if __name__ == "__main__":
    main()
