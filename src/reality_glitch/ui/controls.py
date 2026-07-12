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
}

DEFAULT_SETTINGS: dict[EffectId, dict[str, Any]] = {
    EffectId.WAVE: {"amplitude": 30, "frequency": 3.0, "vertical": False},
    EffectId.GLITCH: {"intensity": 50, "block_count": 22, "seed": 42},
    EffectId.RGB_SPLIT: {"distance": 18},
    EffectId.MIRROR: {"mode": MirrorMode.LEFT.value},
    EffectId.PORTAL: {"repetitions": 6, "scale": 0.72, "rotation": 4},
    EffectId.GRAYSCALE: {},
}


def render_effect_settings(step: EffectStep, index: int) -> EffectStep:
    settings = dict(step.settings)
    prefix = f"step_{index}_{step.effect_id.value}"

    with st.expander(DISPLAY_NAMES[step.effect_id], expanded=True):
        if step.effect_id is EffectId.WAVE:
            settings["amplitude"] = st.slider(
                "עוצמת הגל", 0, 100, int(settings.get("amplitude", 30)),
                key=f"{prefix}_amplitude",
            )
            settings["frequency"] = st.slider(
                "מספר הגלים", 0.5, 12.0,
                float(settings.get("frequency", 3.0)), 0.5,
                key=f"{prefix}_frequency",
            )
            direction = st.radio(
                "כיוון", ["אופקי", "אנכי"],
                index=1 if settings.get("vertical", False) else 0,
                horizontal=True,
                key=f"{prefix}_direction",
            )
            settings["vertical"] = direction == "אנכי"

        elif step.effect_id is EffectId.GLITCH:
            settings["intensity"] = st.slider(
                "עוצמת התזוזה", 1, 180,
                int(settings.get("intensity", 50)),
                key=f"{prefix}_intensity",
            )
            settings["block_count"] = st.slider(
                "מספר אזורים", 1, 80,
                int(settings.get("block_count", 22)),
                key=f"{prefix}_blocks",
            )
            settings["seed"] = int(st.number_input(
                "Seed", 0, 999_999, int(settings.get("seed", 42)),
                key=f"{prefix}_seed",
            ))
            if st.button("Seed אקראי", key=f"{prefix}_random"):
                settings["seed"] = random.randint(0, 999_999)

        elif step.effect_id is EffectId.RGB_SPLIT:
            settings["distance"] = st.slider(
                "מרחק הפרדת הצבעים", 0, 100,
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
                "מספר החזרות", 1, 14,
                int(settings.get("repetitions", 6)),
                key=f"{prefix}_repetitions",
            )
            settings["scale"] = st.slider(
                "יחס ההקטנה", 0.40, 0.90,
                float(settings.get("scale", 0.72)), 0.01,
                key=f"{prefix}_scale",
            )
            settings["rotation"] = st.slider(
                "סיבוב בכל שלב", -20, 20,
                int(settings.get("rotation", 4)),
                key=f"{prefix}_rotation",
            )

    return EffectStep(step.effect_id, settings)
