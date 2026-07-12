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
    EffectId.CENTER_BULGE: "ניפוח מרכזי",
    EffectId.CENTER_PINCH: "כיווץ מרכזי",
    EffectId.LOCAL_TWIRL: "סחרור מקומי",
    EffectId.DOUBLE_EXPOSURE: "Double Exposure",
    EffectId.PALETTE_TRANSPLANT: "Palette Transplant",
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
    EffectId.CENTER_BULGE: {
        "center_x": 50.0,
        "center_y": 45.0,
        "radius": 32.0,
        "strength": 0.65,
        "falloff": 1.8,
    },
    EffectId.CENTER_PINCH: {
        "center_x": 50.0,
        "center_y": 45.0,
        "radius": 32.0,
        "strength": 0.70,
        "falloff": 1.8,
    },
    EffectId.LOCAL_TWIRL: {
        "center_x": 50.0,
        "center_y": 45.0,
        "radius": 30.0,
        "strength": 3.0,
        "falloff": 1.6,
    },
    EffectId.DOUBLE_EXPOSURE: {
        "source_slot": "blend",
        "opacity": 0.45,
        "channel_shift": 8,
        "mix_mode": "screen",
    },
    EffectId.PALETTE_TRANSPLANT: {
        "source_slot": "palette",
        "mode": "gradient",
        "gradient_contrast": 1.15,
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

        elif step.effect_id in {EffectId.CENTER_BULGE, EffectId.CENTER_PINCH, EffectId.LOCAL_TWIRL}:
            settings["center_x"] = st.slider(
                "מרכז אופקי",
                0.0,
                100.0,
                float(settings.get("center_x", 50.0)),
                1.0,
                key=f"{prefix}_center_x",
            )
            settings["center_y"] = st.slider(
                "מרכז אנכי",
                0.0,
                100.0,
                float(settings.get("center_y", 45.0)),
                1.0,
                key=f"{prefix}_center_y",
            )
            settings["radius"] = st.slider(
                "רדיוס השפעה",
                5.0,
                80.0,
                float(settings.get("radius", 32.0)),
                1.0,
                key=f"{prefix}_local_radius",
            )
            if step.effect_id is EffectId.LOCAL_TWIRL:
                settings["strength"] = st.slider(
                    "עוצמת סחרור",
                    -8.0,
                    8.0,
                    float(settings.get("strength", 3.0)),
                    0.1,
                    key=f"{prefix}_local_strength",
                )
            else:
                settings["strength"] = st.slider(
                    "עוצמת עיוות",
                    0.0,
                    2.0,
                    float(settings.get("strength", 0.65)),
                    0.05,
                    key=f"{prefix}_local_strength",
                )
            settings["falloff"] = st.slider(
                "רכות שוליים",
                0.5,
                4.0,
                float(settings.get("falloff", 1.8)),
                0.1,
                key=f"{prefix}_falloff",
            )

        elif step.effect_id is EffectId.DOUBLE_EXPOSURE:
            settings["source_slot"] = st.selectbox(
                "תמונת מקור",
                ["blend", "palette"],
                index=0 if settings.get("source_slot", "blend") == "blend" else 1,
                key=f"{prefix}_source_slot_de",
                format_func=lambda value: "תמונת מיזוג" if value == "blend" else "תמונת פלטה",
            )
            settings["mix_mode"] = st.selectbox(
                "סוג מיזוג",
                ["screen", "blend", "add"],
                index=["screen", "blend", "add"].index(str(settings.get("mix_mode", "screen"))),
                key=f"{prefix}_mix_mode",
                format_func=lambda value: {"screen": "Screen", "blend": "Blend", "add": "Add"}[value],
            )
            settings["opacity"] = st.slider(
                "עוצמת מיזוג",
                0.0,
                1.0,
                float(settings.get("opacity", 0.45)),
                0.05,
                key=f"{prefix}_opacity",
            )
            settings["channel_shift"] = st.slider(
                "היסט ערוצים",
                0,
                40,
                int(settings.get("channel_shift", 8)),
                key=f"{prefix}_channel_shift_de",
            )

        elif step.effect_id is EffectId.PALETTE_TRANSPLANT:
            settings["source_slot"] = st.selectbox(
                "תמונת פלטה",
                ["palette", "blend"],
                index=0 if settings.get("source_slot", "palette") == "palette" else 1,
                key=f"{prefix}_source_slot_pt",
                format_func=lambda value: "תמונת פלטה" if value == "palette" else "תמונת מיזוג",
            )
            settings["mode"] = st.selectbox(
                "סוג מיפוי צבע",
                ["gradient", "duotone"],
                index=0 if settings.get("mode", "gradient") == "gradient" else 1,
                key=f"{prefix}_palette_mode",
                format_func=lambda value: "Gradient" if value == "gradient" else "Duotone",
            )
            settings["gradient_contrast"] = st.slider(
                "עוצמת מיפוי",
                0.5,
                2.5,
                float(settings.get("gradient_contrast", 1.15)),
                0.05,
                key=f"{prefix}_gradient_contrast",
            )

    return EffectStep(step.effect_id, settings)
