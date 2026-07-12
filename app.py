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
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)


def initialize_state() -> None:
    if "editor" not in st.session_state:
        default_preset = CONTAINER.presets.get("מותאם אישית")
        st.session_state.editor = EditorState.from_preset(default_preset)

    pending_preset = st.session_state.pop("pending_preset", None)
    if pending_preset is not None:
        st.session_state.editor = EditorState.from_preset(
            CONTAINER.presets.get(pending_preset)
        )
        st.session_state.preset_selector = pending_preset

    if "preset_selector" not in st.session_state:
        st.session_state.preset_selector = st.session_state.editor.active_preset

    if "show_pipeline_steps" not in st.session_state:
        st.session_state.show_pipeline_steps = True

    if "gif_data" not in st.session_state:
        st.session_state.gif_data = None

    if "gif_signature" not in st.session_state:
        st.session_state.gif_signature = None


def clear_generated_gif() -> None:
    st.session_state.gif_data = None
    st.session_state.gif_signature = None


def load_preset(name: str) -> None:
    """Load a preset without mutating an already-rendered widget key."""
    st.session_state.editor = EditorState.from_preset(CONTAINER.presets.get(name))
    clear_generated_gif()


def queue_preset(name: str) -> None:
    """Apply a preset safely at the beginning of the next rerun."""
    st.session_state.pending_preset = name
    clear_generated_gif()


def choose_random_preset() -> None:
    names = [
        preset.name
        for preset in CONTAINER.presets.list_all()
        if preset.name != "מותאם אישית"
    ]
    queue_preset(random.choice(names))


def reset_editor() -> None:
    queue_preset("מותאם אישית")


def build_effect_options() -> list[EffectId]:
    return list(EffectId)


def add_effect_to_editor(effect_id: EffectId) -> None:
    editor: EditorState = st.session_state.editor
    if len(editor.steps) >= 6:
        return
    editor.steps.append(EffectStep(effect_id, dict(DEFAULT_SETTINGS[effect_id])))
    editor.active_preset = "מותאם אישית"
    clear_generated_gif()


def remove_effect_from_editor(index: int) -> None:
    editor: EditorState = st.session_state.editor
    if 0 <= index < len(editor.steps):
        editor.steps.pop(index)
        editor.active_preset = "מותאם אישית"
        clear_generated_gif()


def move_effect(index: int, direction: int) -> None:
    editor: EditorState = st.session_state.editor
    new_index = index + direction
    if 0 <= index < len(editor.steps) and 0 <= new_index < len(editor.steps):
        editor.steps[index], editor.steps[new_index] = (
            editor.steps[new_index],
            editor.steps[index],
        )
        editor.active_preset = "מותאם אישית"
        clear_generated_gif()


def clear_pipeline() -> None:
    editor: EditorState = st.session_state.editor
    editor.steps = []
    editor.active_preset = "מותאם אישית"
    clear_generated_gif()


def render_pipeline_card(step: EffectStep, index: int, total: int) -> None:
    st.markdown(
        f"""
        <div class="effect-card-title">
            <div class="effect-card-index">{index + 1}</div>
            <div class="effect-card-name">{DISPLAY_NAMES[step.effect_id]}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    up_col, down_col, remove_col = st.columns([0.9, 0.9, 1.3])
    with up_col:
        if st.button("⬆ למעלה", key=f"move_up_{index}", use_container_width=True, disabled=index == 0):
            move_effect(index, -1)
            st.rerun()
    with down_col:
        if st.button("⬇ למטה", key=f"move_down_{index}", use_container_width=True, disabled=index == total - 1):
            move_effect(index, 1)
            st.rerun()
    with remove_col:
        if st.button("✕ הסרה", key=f"remove_effect_{index}", use_container_width=True):
            remove_effect_from_editor(index)
            st.rerun()


def build_pipeline_summary(steps: list[EffectStep]) -> str:
    if not steps:
        return "בחרו לפחות אפקט אחד"
    return "  ◀  ".join(DISPLAY_NAMES[step.effect_id] for step in steps)


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
        <section class="energy-hero">
            <div class="hero-orb orb-one"></div>
            <div class="hero-orb orb-two"></div>
            <div class="energy-copy">
                <span class="energy-kicker">CREATIVE IMAGE LAB</span>
                <h1>Reality Glitch <em>Studio</em></h1>
                <p>מעלים תמונה, משחקים עם המציאות ויוצרים משהו שאף אחד אחר לא יקבל.</p>
                <div class="hero-pills">
                    <span>{effect_count} אפקטים</span>
                    <span>{preset_count} סגנונות</span>
                    <span>PNG</span>
                    <span>GIF</span>
                </div>
            </div>
            <div class="hero-spark">✦</div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_header() -> None:
    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="brand-mark">R</div>
            <div>
                <strong>Reality Glitch</strong>
                <span>סטודיו יצירתי בפייתון</span>
            </div>
        </div>
        <div class="start-here">
            <span class="start-dot"></span>
            מתחילים כאן - מעלים תמונה
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_section_heading(number: int, title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="control-heading">
            <span>{number}</span>
            <div><strong>{title}</strong><small>{subtitle}</small></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_empty_state() -> None:
    st.markdown(
        """
        <section class="launch-zone">
            <div class="launch-symbol">↥</div>
            <div>
                <span class="launch-label">START HERE</span>
                <h2>בחרו תמונה והתחילו לשנות את המציאות</h2>
                <p>האפקטים פועלים מיד, ואפשר לבנות שילוב אישי ולהנפיש אותו.</p>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    cards = [
        ("01", "מעלים", "JPG, PNG או WEBP"),
        ("02", "משנים", "Preset או אפקטים אישיים"),
        ("03", "מנפישים", "GIF חי בלחיצה"),
        ("04", "מורידים", "PNG או GIF"),
    ]
    columns = st.columns(4)
    for column, (number, title, text) in zip(columns, cards):
        with column:
            st.markdown(
                f"""
                <div class="journey-card">
                    <span>{number}</span><strong>{title}</strong><small>{text}</small>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_sidebar() -> tuple[Any, EditorState, bool]:
    editor: EditorState = st.session_state.editor

    with st.sidebar:
        render_sidebar_header()

        render_section_heading(1, "תמונה", "בחרו חומר גלם")
        uploaded_file = st.file_uploader(
            "העלאת תמונה",
            type=["jpg", "jpeg", "png", "webp"],
            help="התמונה מוקטנת אוטומטית לשמירה על ביצועים בענן.",
            label_visibility="collapsed",
        )

        quick_left, quick_right = st.columns(2)
        with quick_left:
            if st.button("הפתע אותי", use_container_width=True):
                choose_random_preset()
                st.rerun()
        with quick_right:
            if st.button("איפוס", use_container_width=True):
                reset_editor()
                st.rerun()

        render_section_heading(2, "אפקטים", "בנו רצף משלכם")
        add_col, clear_col = st.columns([1.65, 0.75])
        with add_col:
            selected_to_add = st.selectbox(
                "אפקט להוספה",
                build_effect_options(),
                key="effect_to_add_selector",
                format_func=DISPLAY_NAMES.get,
                label_visibility="collapsed",
            )
        with clear_col:
            if st.button("נקה", key="clear_pipeline", use_container_width=True, disabled=not editor.steps):
                clear_pipeline()
                st.rerun()

        if st.button("➕ הוספת אפקט", key="add_effect_button", use_container_width=True):
            add_effect_to_editor(selected_to_add)
            st.rerun()

        st.caption("האפקטים פועלים מלמעלה למטה. אפשר להזיז, להסיר או להוסיף עד 6 אפקטים.")

        st.markdown(
            f'<div class="pipeline-ribbon">{build_pipeline_summary(editor.steps)}</div>',
            unsafe_allow_html=True,
        )

        edited_steps: list[EffectStep] = []
        total_steps = len(editor.steps)
        for index, step in enumerate(editor.steps):
            st.markdown('<div class="effect-card">', unsafe_allow_html=True)
            render_pipeline_card(step, index, total_steps)
            edited_steps.append(render_effect_settings(step, index))
            st.markdown('</div>', unsafe_allow_html=True)

        render_section_heading(3, "גימור", "הטאץ׳ האחרון")
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

        st.markdown(
            """
            <div class="sidebar-tip">
                <b>טיפ</b>
                האפקטים החדשים המקומיים עובדים הכי טוב כשהאובייקט הראשי קרוב למרכז.
            </div>
            """,
            unsafe_allow_html=True,
        )

        render_section_heading(4, "פריסטים", "קיצור דרך לתוצאה מוכנה")
        preset_names = [preset.name for preset in CONTAINER.presets.list_all()]
        st.selectbox(
            "Preset",
            preset_names,
            key="preset_selector",
            label_visibility="collapsed",
        )
        if st.button(
            "הפעלת הסגנון",
            type="primary",
            use_container_width=True,
            key="apply_preset",
        ):
            load_preset(st.session_state.preset_selector)
            st.rerun()

        editor.steps = edited_steps
        if editor.active_preset != "מותאם אישית":
            editor.active_preset = "מותאם אישית" if edited_steps != list(CONTAINER.presets.get(editor.active_preset).steps) else editor.active_preset
        editor.finish = FinishSettings(contrast, color)

    return uploaded_file, editor, show_steps


def render_image_metadata(original: Image.Image, step_count: int) -> None:
    width, height = original.size
    cards = [
        ("רזולוציה", f"{width} × {height}"),
        ("Pipeline", f"{step_count} שלבים"),
        ("צבע", original.mode),
    ]
    columns = st.columns(3)
    for column, (label, value) in zip(columns, cards):
        with column:
            st.markdown(
                f"""
                <div class="info-tile"><span>{label}</span><strong>{value}</strong></div>
                """,
                unsafe_allow_html=True,
            )


def render_studio(original: Image.Image, result_image: Image.Image) -> None:
    st.markdown(
        '<div class="section-banner"><span>LIVE PREVIEW</span><h2>לפני ואחרי</h2></div>',
        unsafe_allow_html=True,
    )
    source_column, result_column = st.columns(2, gap="large")
    with source_column:
        st.markdown('<div class="image-label source">מקור</div>', unsafe_allow_html=True)
        st.image(original, use_container_width=True)
    with result_column:
        st.markdown('<div class="image-label result">תוצאה</div>', unsafe_allow_html=True)
        st.image(result_image, use_container_width=True)


def render_steps(result_steps: tuple[Any, ...]) -> None:
    st.markdown(
        '<div class="section-banner compact"><span>PIPELINE</span><h2>איך נבנתה התוצאה</h2></div>',
        unsafe_allow_html=True,
    )
    if not result_steps:
        st.info("הפעילו 'הצגת שלבי ביניים' בפאנל כדי לראות כל שלב.")
        return

    columns = st.columns(min(3, len(result_steps)))
    for index, step_result in enumerate(result_steps):
        with columns[index % len(columns)]:
            st.markdown(
                f"""
                <div class="step-card-title">
                    <span>{index + 1}</span>
                    <strong>{DISPLAY_NAMES[step_result.effect_id]}</strong>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.image(step_result.image, use_container_width=True)


def render_export_center(
    original: Image.Image,
    result_image: Image.Image,
    editor: EditorState,
    uploaded_bytes: bytes,
) -> None:
    st.markdown(
        """
        <div class="export-hero">
            <div><span>READY TO SHARE</span><h2>מורידים תמונה או מנפישים אותה</h2></div>
            <div class="export-badge">PNG + GIF</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    png_column, gif_column = st.columns([0.8, 1.2], gap="large")

    with png_column:
        st.markdown(
            """
            <div class="download-copy">
                <span class="download-icon">▣</span>
                <h3>תמונה סטטית</h3>
                <p>התוצאה המדויקת שמופיעה בתצוגה.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.download_button(
            "הורדת PNG",
            CONTAINER.exporter.to_png(result_image),
            "reality-glitch.png",
            "image/png",
            type="primary",
            use_container_width=True,
        )

    with gif_column:
        st.markdown(
            """
            <div class="download-copy gif-copy">
                <span class="download-icon">▶</span>
                <h3>GIF מונפש</h3>
                <p>האפקטים נבנים בהדרגה וחוזרים בלולאה.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        settings_left, settings_right = st.columns(2)
        with settings_left:
            frame_count = st.slider(
                "מספר פריימים",
                5,
                24,
                12,
                key="gif_frame_count",
            )
        with settings_right:
            frame_duration = st.slider(
                "מהירות",
                50,
                300,
                90,
                10,
                key="gif_frame_duration",
                help="מספר נמוך יותר יוצר אנימציה מהירה יותר.",
            )

        options = AnimationOptions(frame_count, frame_duration)
        request = PipelineRequest(tuple(editor.steps), editor.finish)
        signature = build_render_signature(uploaded_bytes, request, options)

        create_clicked = st.button(
            "⚡ יצירת GIF עכשיו",
            type="primary",
            use_container_width=True,
            key="create_gif",
        )
        if create_clicked:
            try:
                with st.spinner("מייצר את האנימציה המלאה..."):
                    st.session_state.gif_data = CONTAINER.animation.render_gif(
                        original,
                        request,
                        options,
                    )
                    st.session_state.gif_signature = signature
            except (RealityGlitchError, OSError, ValueError) as error:
                LOGGER.exception("Failed to generate GIF")
                st.error("לא הצלחנו ליצור את ה-GIF.")
                with st.expander("פרטי השגיאה"):
                    st.code(str(error))

        if (
            st.session_state.gif_data is not None
            and st.session_state.gif_signature == signature
        ):
            st.success("ה-GIF מוכן")
            st.image(st.session_state.gif_data, use_container_width=True)
            st.download_button(
                "הורדת GIF",
                st.session_state.gif_data,
                "reality-glitch-animation.gif",
                "image/gif",
                type="primary",
                use_container_width=True,
            )
        elif st.session_state.gif_data is not None:
            st.warning("שיניתם הגדרות. לחצו שוב על יצירת GIF כדי לרענן אותו.")


def main() -> None:
    initialize_state()
    apply_styles()
    render_header()

    uploaded_file, editor, show_steps = render_sidebar()
    if uploaded_file is None:
        render_empty_state()
        return
    if not editor.steps:
        st.warning("יש לבחור לפחות אפקט אחד בפאנל השמאלי.")
        return

    uploaded_bytes = uploaded_file.getvalue()

    try:
        with st.spinner("הסטודיו מעבד את התמונה..."):
            original = CONTAINER.image_service.prepare(Image.open(uploaded_file))
            request = PipelineRequest(
                steps=tuple(editor.steps),
                finish=editor.finish,
                include_intermediate_steps=show_steps,
            )
            result = CONTAINER.pipeline.execute(original, request)
    except (RealityGlitchError, UnidentifiedImageError, OSError, ValueError) as error:
        LOGGER.exception("Failed to process image")
        st.error("לא הצלחנו לעבד את התמונה. בדקו את הקובץ וההגדרות.")
        with st.expander("פרטי השגיאה"):
            st.code(str(error))
        return

    render_image_metadata(original, len(editor.steps))

    studio_tab, steps_tab, export_tab = st.tabs(
        ["⚡ הסטודיו", "◉ שלבי היצירה", "↗ יצוא ו-GIF"]
    )

    with studio_tab:
        render_studio(original, result.image)
        st.markdown('<div class="quick-export-line">התוצאה מוכנה - עברו לטאב יצוא ו-GIF כדי להוריד או להנפיש.</div>', unsafe_allow_html=True)

    with steps_tab:
        render_steps(result.steps)

    with export_tab:
        render_export_center(
            original,
            result.image,
            editor,
            uploaded_bytes,
        )


if __name__ == "__main__":
    main()
