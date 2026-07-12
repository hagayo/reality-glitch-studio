from __future__ import annotations

import hashlib
import logging
import random
from typing import Any

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
APP_TITLE = "Reality Glitch Studio"
CONTAINER = build_container()

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🌀",
    layout="wide",
    initial_sidebar_state="expanded",
)


def initialize_state() -> None:
    if "editor" not in st.session_state:
        default_preset = CONTAINER.presets.get("מותאם אישית")
        st.session_state.editor = EditorState.from_preset(default_preset)

    if "preset_selector" not in st.session_state:
        st.session_state.preset_selector = st.session_state.editor.active_preset

    if "show_pipeline_steps" not in st.session_state:
        st.session_state.show_pipeline_steps = True

    if "gif_data" not in st.session_state:
        st.session_state.gif_data = None

    if "gif_signature" not in st.session_state:
        st.session_state.gif_signature = None


def load_preset(name: str) -> None:
    st.session_state.editor = EditorState.from_preset(
        CONTAINER.presets.get(name)
    )
    st.session_state.preset_selector = name
    clear_generated_gif()


def clear_generated_gif() -> None:
    st.session_state.gif_data = None
    st.session_state.gif_signature = None


def choose_random_preset() -> None:
    names = [
        preset.name
        for preset in CONTAINER.presets.list_all()
        if preset.name != "מותאם אישית"
    ]
    load_preset(random.choice(names))


def reset_editor() -> None:
    load_preset("מותאם אישית")


def build_pipeline_summary(steps: list[EffectStep]) -> str:
    if not steps:
        return "לא נבחרו אפקטים"
    return " ← ".join(DISPLAY_NAMES[step.effect_id] for step in steps)


def build_render_signature(
    uploaded_bytes: bytes,
    request: PipelineRequest,
    options: AnimationOptions,
) -> str:
    payload = (
        uploaded_bytes
        + repr(request).encode("utf-8")
        + repr(options).encode("utf-8")
    )
    return hashlib.sha256(payload).hexdigest()


def render_header() -> None:
    effect_count = len(CONTAINER.registry.list_definitions())
    preset_count = len(CONTAINER.presets.list_all())

    st.markdown(
        f"""
        <section class="hero-shell">
            <div class="hero-copy">
                <span class="eyebrow">CREATIVE PYTHON LAB</span>
                <h1>{APP_TITLE}</h1>
                <p>מעלים תמונה, בונים שרשרת אפקטים ומפיקים יצירה חדשה בזמן אמת.</p>
            </div>
            <div class="hero-stats">
                <div class="stat-card"><strong>{effect_count}</strong><span>אפקטים</span></div>
                <div class="stat-card"><strong>{preset_count}</strong><span>Presets</span></div>
                <div class="stat-card"><strong>PNG + GIF</strong><span>יצוא</span></div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_empty_state() -> None:
    st.markdown(
        """
        <section class="empty-state">
            <div class="empty-icon">✦</div>
            <h2>הסטודיו מוכן</h2>
            <p>העלו תמונה מהסרגל הצדדי ובחרו Preset להתחלה מהירה.</p>
        </section>
        """,
        unsafe_allow_html=True,
    )

    first, second, third = st.columns(3)
    with first:
        st.markdown(
            '<div class="feature-card"><b>1. מעלים</b><span>JPG, PNG או WEBP</span></div>',
            unsafe_allow_html=True,
        )
    with second:
        st.markdown(
            '<div class="feature-card"><b>2. מעצבים</b><span>Preset או Pipeline אישי</span></div>',
            unsafe_allow_html=True,
        )
    with third:
        st.markdown(
            '<div class="feature-card"><b>3. מורידים</b><span>תמונה או אנימציה</span></div>',
            unsafe_allow_html=True,
        )


def render_sidebar() -> tuple[Any, EditorState, bool]:
    editor: EditorState = st.session_state.editor

    with st.sidebar:
        st.markdown('<div class="sidebar-title">לוח הבקרה</div>', unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "בחירת תמונה",
            type=["jpg", "jpeg", "png", "webp"],
            help="התמונה מוקטנת אוטומטית כדי לשמור על ביצועים טובים בענן.",
        )

        st.markdown("#### התחלה מהירה")
        quick_left, quick_right = st.columns(2)
        with quick_left:
            if st.button("הפתע אותי", use_container_width=True):
                choose_random_preset()
                st.rerun()
        with quick_right:
            if st.button("איפוס", use_container_width=True):
                reset_editor()
                st.rerun()

        preset_names = [preset.name for preset in CONTAINER.presets.list_all()]
        st.selectbox(
            "Preset",
            preset_names,
            key="preset_selector",
        )
        if st.button("הפעלת ה-Preset", type="primary", use_container_width=True):
            load_preset(st.session_state.preset_selector)
            st.rerun()

        st.divider()
        st.markdown("#### בניית Pipeline")

        selected_ids = st.multiselect(
            "אפקטים לפי סדר הפעלה",
            list(EffectId),
            default=[step.effect_id for step in editor.steps],
            max_selections=4,
            format_func=DISPLAY_NAMES.get,
            help="סדר הבחירה הוא סדר הפעלת האפקטים.",
        )

        existing = {step.effect_id: step for step in editor.steps}
        steps = [
            existing.get(
                effect_id,
                EffectStep(effect_id, dict(DEFAULT_SETTINGS[effect_id])),
            )
            for effect_id in selected_ids
        ]

        st.markdown(
            f'<div class="pipeline-box">{build_pipeline_summary(steps)}</div>',
            unsafe_allow_html=True,
        )

        edited_steps = [
            render_effect_settings(step, index)
            for index, step in enumerate(steps)
        ]

        st.divider()
        st.markdown("#### גימור")
        contrast = st.slider(
            "ניגודיות",
            0.5,
            2.0,
            float(editor.finish.contrast),
            0.05,
        )
        color = st.slider(
            "עוצמת צבע",
            0.0,
            2.5,
            float(editor.finish.color),
            0.05,
        )
        show_steps = st.toggle(
            "הצגת שלבי ביניים",
            value=st.session_state.show_pipeline_steps,
        )
        st.session_state.show_pipeline_steps = show_steps

        editor.steps = edited_steps
        editor.finish = FinishSettings(contrast, color)

    return uploaded_file, editor, show_steps


def render_image_metadata(original: Image.Image, step_count: int) -> None:
    width, height = original.size
    first, second, third = st.columns(3)
    first.metric("רזולוציה", f"{width} × {height}")
    second.metric("שלבים", step_count)
    third.metric("מצב צבע", original.mode)


def render_studio_tab(original: Image.Image, result_image: Image.Image) -> None:
    source_column, result_column = st.columns(2, gap="large")
    with source_column:
        st.markdown("#### המקור")
        st.image(original, use_container_width=True)
    with result_column:
        st.markdown("#### התוצאה")
        st.image(result_image, use_container_width=True)


def render_steps_tab(result_steps: tuple[Any, ...]) -> None:
    if not result_steps:
        st.info("לא נשמרו שלבי ביניים להרצה הזו.")
        return

    columns = st.columns(min(3, len(result_steps)))
    for index, step_result in enumerate(result_steps):
        with columns[index % len(columns)]:
            st.markdown(
                f'<div class="step-number">שלב {index + 1}</div>',
                unsafe_allow_html=True,
            )
            st.caption(DISPLAY_NAMES[step_result.effect_id])
            st.image(step_result.image, use_container_width=True)


def render_export_tab(
    original: Image.Image,
    result_image: Image.Image,
    editor: EditorState,
    uploaded_bytes: bytes,
) -> None:
    png_column, gif_column = st.columns(2, gap="large")

    with png_column:
        st.markdown("### תמונה סטטית")
        st.caption("הורדה מידית באיכות התוצאה המוצגת.")
        st.download_button(
            "הורדת PNG",
            CONTAINER.exporter.to_png(result_image),
            "reality-glitch.png",
            "image/png",
            type="primary",
            use_container_width=True,
        )

    with gif_column:
        st.markdown("### אנימציה")
        frame_count = st.slider(
            "מספר פריימים",
            5,
            24,
            12,
            key="gif_frame_count",
        )
        frame_duration = st.slider(
            "משך פריים במילישניות",
            50,
            300,
            90,
            10,
            key="gif_frame_duration",
        )

        options = AnimationOptions(frame_count, frame_duration)
        request = PipelineRequest(tuple(editor.steps), editor.finish)
        signature = build_render_signature(uploaded_bytes, request, options)

        if st.button("יצירת GIF", use_container_width=True):
            with st.spinner("יוצר את האנימציה..."):
                st.session_state.gif_data = CONTAINER.animation.render_gif(
                    original,
                    request,
                    options,
                )
                st.session_state.gif_signature = signature

        if (
            st.session_state.gif_data is not None
            and st.session_state.gif_signature == signature
        ):
            st.image(st.session_state.gif_data)
            st.download_button(
                "הורדת GIF",
                st.session_state.gif_data,
                "reality-glitch-animation.gif",
                "image/gif",
                type="primary",
                use_container_width=True,
            )
        elif st.session_state.gif_data is not None:
            st.info("ההגדרות השתנו. צרו מחדש את ה-GIF כדי לעדכן אותו.")


def main() -> None:
    initialize_state()
    apply_styles()
    render_header()

    uploaded_file, editor, show_steps = render_sidebar()
    if uploaded_file is None:
        render_empty_state()
        return
    if not editor.steps:
        st.warning("יש לבחור לפחות אפקט אחד.")
        return

    uploaded_bytes = uploaded_file.getvalue()

    try:
        with st.spinner("מעבד את התמונה..."):
            original = CONTAINER.image_service.prepare(Image.open(uploaded_file))
            request = PipelineRequest(
                steps=tuple(editor.steps),
                finish=editor.finish,
                include_intermediate_steps=show_steps,
            )
            result = CONTAINER.pipeline.execute(original, request)
    except (RealityGlitchError, UnidentifiedImageError, OSError, ValueError) as error:
        LOGGER.exception("Failed to process image")
        st.error("לא הצלחנו לעבד את התמונה. בדקו שהקובץ וההגדרות תקינים.")
        with st.expander("פרטי השגיאה"):
            st.code(str(error))
        return

    render_image_metadata(original, len(editor.steps))

    studio_tab, steps_tab, export_tab = st.tabs(
        ["סטודיו", "שלבי Pipeline", "הורדה ו-GIF"]
    )

    with studio_tab:
        render_studio_tab(original, result.image)

    with steps_tab:
        render_steps_tab(result.steps)

    with export_tab:
        render_export_tab(
            original,
            result.image,
            editor,
            uploaded_bytes,
        )


if __name__ == "__main__":
    main()
