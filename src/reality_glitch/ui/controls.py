from __future__ import annotations

import random
from typing import Any

import streamlit as st

from reality_glitch.domain.models import EffectId, EffectStep, MirrorMode


DISPLAY_NAMES = {
    EffectId.WAVE: "גל במציאות",
    EffectId.GLITCH: "התפרקות דיגיטלית",
    EffectId.RGB_SPLIT: "הפרדת צבעים",
    EffectId.MIRROR: "מראה בלתי אפשרית",
    EffectId.PORTAL: "פורטל אינסופי",
    EffectId.GRAYSCALE: "שחור לבן",
    EffectId.PIXEL_SORT: "מיון פיקסלים",
    EffectId.KALEIDOSCOPE: "קליידוסקופ",
    EffectId.CIRCULAR_RIPPLE: "גלים מעגליים",
    EffectId.MOSAIC: "פסיפס",
    EffectId.SWIRL: "סחרור",
    EffectId.RETRO_CRT: "מסך CRT",
}

DEFAULT_SETTINGS: dict[EffectId, dict[str, Any]] = {
    EffectId.WAVE: {"amplitude": 30, "frequency": 3.0, "vertical": False},
    EffectId.GLITCH: {"intensity": 50, "block_count": 22, "seed": 42},
    EffectId.RGB_SPLIT: {"distance": 18},
    EffectId.MIRROR: {"mode": MirrorMode.LEFT.value},
    EffectId.PORTAL: {"repetitions": 6, "scale": 0.72, "rotation": 4},
    EffectId.GRAYSCALE: {},
    EffectId.PIXEL_SORT: {
        "orientation": "horizontal",
        "threshold": 110,
        "reverse": False,
        "min_segment_length": 8,
    },
    EffectId.KALEIDOSCOPE: {
        "segments": 6,
        "rotation_degrees": 0.0,
        "zoom": 1.0,
    },
    EffectId.CIRCULAR_RIPPLE: {
        "amplitude": 18,
        "wavelength": 40,
        "phase_degrees": 0.0,
    },
    EffectId.MOSAIC: {
        "block_size": 12,
    },
    EffectId.SWIRL: {
        "strength": 3.5,
        "radius": 180.0,
    },
    EffectId.RETRO_CRT: {
        "scanline_strength": 0.22,
        "line_spacing": 3,
        "channel_shift": 2,
        "noise_strength": 0.02,
        "seed": 42,
    },
}


def render_effect_settings(step: EffectStep, index: int) -> EffectStep:
    settings = dict(step.settings)
    prefix = f"step_{index}_{step.effect_id.value}"

    with st.expander(DISPLAY_NAMES[step.effect_id], expanded=True):
        if step.effect_id is EffectId.WAVE:
            settings["amplitude"] = st.slider(
                "עוצמת הגל",
                0,
                100,
                int(settings.get("amplitude", 30)),
                key=f"{prefix}_amplitude",
            )
            settings["frequency"] = st.slider(
                "מספר הגלים",
                0.5,
                12.0,
                float(settings.get("frequency", 3.0)),
                0.5,
                key=f"{prefix}_frequency",
            )
            direction = st.radio(
                "כיוון",
                ["אופקי", "אנכי"],
                index=1 if settings.get("vertical", False) else 0,
                horizontal=True,
                key=f"{prefix}_direction",
            )
            settings["vertical"] = direction == "אנכי"

        elif step.effect_id is EffectId.GLITCH:
            settings["intensity"] = st.slider(
                "עוצמת התזוזה",
                1,
                180,
                int(settings.get("intensity", 50)),
                key=f"{prefix}_intensity",
            )
            settings["block_count"] = st.slider(
                "מספר אזורים",
                1,
                80,
                int(settings.get("block_count", 22)),
                key=f"{prefix}_blocks",
            )
            settings["seed"] = int(
                st.number_input(
                    "Seed",
                    0,
                    999_999,
                    int(settings.get("seed", 42)),
                    key=f"{prefix}_seed",
                )
            )
            if st.button("Seed אקראי", key=f"{prefix}_random"):
                settings["seed"] = random.randint(0, 999_999)

        elif step.effect_id is EffectId.RGB_SPLIT:
            settings["distance"] = st.slider(
                "מרחק הפרדת הצבעים",
                0,
                100,
                int(settings.get("distance", 18)),
                key=f"{prefix}_distance",
            )

        elif step.effect_id is EffectId.MIRROR:
            labels = {
                MirrorMode.LEFT.value: "צד שמאל",
                MirrorMode.RIGHT.value: "צד ימין",
                MirrorMode.TOP.value: "החלק העליון",
                MirrorMode.BOTTOM.value: "החלק התחתון",
            }
            current = str(settings.get("mode", MirrorMode.LEFT.value))
            selected = st.selectbox(
                "איזה חלק ישוכפל?",
                list(labels),
                index=list(labels).index(current),
                format_func=labels.get,
                key=f"{prefix}_mode",
            )
            settings["mode"] = selected

        elif step.effect_id is EffectId.GRAYSCALE:
            st.caption("האפקט ממיר את התמונה לשחור-לבן אמיתי.")

        elif step.effect_id is EffectId.PORTAL:
            settings["repetitions"] = st.slider(
                "מספר החזרות",
                1,
                14,
                int(settings.get("repetitions", 6)),
                key=f"{prefix}_repetitions",
            )
            settings["scale"] = st.slider(
                "יחס ההקטנה",
                0.40,
                0.90,
                float(settings.get("scale", 0.72)),
                0.01,
                key=f"{prefix}_scale",
            )
            settings["rotation"] = st.slider(
                "סיבוב בכל שלב",
                -20,
                20,
                int(settings.get("rotation", 4)),
                key=f"{prefix}_rotation",
            )

        elif step.effect_id is EffectId.PIXEL_SORT:
            settings["orientation"] = st.radio(
                "כיוון המיון",
                ["horizontal", "vertical"],
                index=0 if settings.get("orientation", "horizontal") == "horizontal" else 1,
                horizontal=True,
                key=f"{prefix}_orientation",
                format_func=lambda value: "אופקי" if value == "horizontal" else "אנכי",
            )
            settings["threshold"] = st.slider(
                "סף בהירות למיון",
                0,
                255,
                int(settings.get("threshold", 110)),
                key=f"{prefix}_threshold",
            )
            settings["reverse"] = st.checkbox(
                "מיון הפוך",
                value=bool(settings.get("reverse", False)),
                key=f"{prefix}_reverse",
            )
            settings["min_segment_length"] = st.slider(
                "אורך מינימלי למקטע",
                1,
                64,
                int(settings.get("min_segment_length", 8)),
                key=f"{prefix}_min_segment_length",
            )

        elif step.effect_id is EffectId.KALEIDOSCOPE:
            settings["segments"] = st.slider(
                "מספר פלחים",
                2,
                16,
                int(settings.get("segments", 6)),
                key=f"{prefix}_segments",
            )
            settings["rotation_degrees"] = st.slider(
                "זווית סיבוב",
                0.0,
                360.0,
                float(settings.get("rotation_degrees", 0.0)),
                1.0,
                key=f"{prefix}_rotation_degrees",
            )
            settings["zoom"] = st.slider(
                "זום",
                0.4,
                1.5,
                float(settings.get("zoom", 1.0)),
                0.05,
                key=f"{prefix}_zoom",
            )

        elif step.effect_id is EffectId.CIRCULAR_RIPPLE:
            settings["amplitude"] = st.slider(
                "עוצמת הגלים",
                0,
                80,
                int(settings.get("amplitude", 18)),
                key=f"{prefix}_ripple_amplitude",
            )
            settings["wavelength"] = st.slider(
                "אורך גל",
                4,
                200,
                int(settings.get("wavelength", 40)),
                key=f"{prefix}_wavelength",
            )
            settings["phase_degrees"] = st.slider(
                "פאזה",
                0.0,
                360.0,
                float(settings.get("phase_degrees", 0.0)),
                1.0,
                key=f"{prefix}_phase",
            )

        elif step.effect_id is EffectId.MOSAIC:
            settings["block_size"] = st.slider(
                "גודל אריח",
                1,
                60,
                int(settings.get("block_size", 12)),
                key=f"{prefix}_block_size",
            )

        elif step.effect_id is EffectId.SWIRL:
            settings["strength"] = st.slider(
                "עוצמת הסחרור",
                0.0,
                12.0,
                float(settings.get("strength", 3.5)),
                0.1,
                key=f"{prefix}_strength",
            )
            settings["radius"] = st.slider(
                "רדיוס הסחרור",
                10.0,
                600.0,
                float(settings.get("radius", 180.0)),
                5.0,
                key=f"{prefix}_radius",
            )

        elif step.effect_id is EffectId.RETRO_CRT:
            settings["scanline_strength"] = st.slider(
                "עוצמת קווי סריקה",
                0.0,
                0.8,
                float(settings.get("scanline_strength", 0.22)),
                0.01,
                key=f"{prefix}_scanline_strength",
            )
            settings["line_spacing"] = st.slider(
                "ריווח קווים",
                1,
                12,
                int(settings.get("line_spacing", 3)),
                key=f"{prefix}_line_spacing",
            )
            settings["channel_shift"] = st.slider(
                "היסט ערוצי צבע",
                0,
                12,
                int(settings.get("channel_shift", 2)),
                key=f"{prefix}_channel_shift",
            )
            settings["noise_strength"] = st.slider(
                "רעש",
                0.0,
                0.2,
                float(settings.get("noise_strength", 0.02)),
                0.005,
                key=f"{prefix}_noise_strength",
            )
            settings["seed"] = int(
                st.number_input(
                    "Seed CRT",
                    0,
                    999_999,
                    int(settings.get("seed", 42)),
                    key=f"{prefix}_crt_seed",
                )
            )

    return EffectStep(step.effect_id, settings)
