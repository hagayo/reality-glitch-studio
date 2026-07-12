from __future__ import annotations

from reality_glitch.domain.exceptions import UnknownPresetError
from reality_glitch.domain.models import (
    EffectId,
    EffectStep,
    FinishSettings,
    MirrorMode,
    Preset,
)


class InMemoryPresetRepository:
    def __init__(self) -> None:
        self._presets = {
            preset.name: preset
            for preset in self._build_presets()
        }

    def list_all(self) -> tuple[Preset, ...]:
        return tuple(self._presets.values())

    def get(self, name: str) -> Preset:
        try:
            return self._presets[name]
        except KeyError as error:
            raise UnknownPresetError(f"Unknown preset: {name}") from error

    @staticmethod
    def _build_presets() -> tuple[Preset, ...]:
        return (
            Preset(
                name="מותאם אישית",
                steps=(
                    EffectStep(
                        EffectId.WAVE,
                        {"amplitude": 30, "frequency": 3.0, "vertical": False},
                    ),
                    EffectStep(EffectId.RGB_SPLIT, {"distance": 18}),
                ),
                finish=FinishSettings(contrast=1.0, color=1.1),
            ),
            Preset(
                name="Cyber Pulse",
                steps=(
                    EffectStep(EffectId.RGB_SPLIT, {"distance": 32}),
                    EffectStep(
                        EffectId.GLITCH,
                        {"intensity": 70, "block_count": 28, "seed": 8172},
                    ),
                ),
                finish=FinishSettings(contrast=1.25, color=1.65),
            ),
            Preset(
                name="Dream Portal",
                steps=(
                    EffectStep(
                        EffectId.PORTAL,
                        {"repetitions": 8, "scale": 0.76, "rotation": 5},
                    ),
                    EffectStep(
                        EffectId.WAVE,
                        {"amplitude": 14, "frequency": 2.0, "vertical": False},
                    ),
                ),
                finish=FinishSettings(contrast=1.05, color=1.25),
            ),
            Preset(
                name="Broken Reality",
                steps=(
                    EffectStep(EffectId.MIRROR, {"mode": MirrorMode.RIGHT.value}),
                    EffectStep(
                        EffectId.GLITCH,
                        {"intensity": 95, "block_count": 35, "seed": 404},
                    ),
                    EffectStep(EffectId.RGB_SPLIT, {"distance": 24}),
                ),
                finish=FinishSettings(contrast=1.35, color=1.4),
            ),
            Preset(
                name="Liquid Signal",
                steps=(
                    EffectStep(
                        EffectId.WAVE,
                        {"amplitude": 42, "frequency": 5.5, "vertical": True},
                    ),
                    EffectStep(EffectId.RGB_SPLIT, {"distance": 12}),
                    EffectStep(
                        EffectId.PORTAL,
                        {"repetitions": 4, "scale": 0.68, "rotation": -3},
                    ),
                ),
                finish=FinishSettings(contrast=1.1, color=1.5),
            ),
            Preset(
                name="Mirror Gloss",
                steps=(
                    EffectStep(EffectId.MIRROR, {"mode": MirrorMode.RIGHT.value}),
                    EffectStep(
                        EffectId.PORTAL,
                        {"repetitions": 3, "scale": 0.8, "rotation": 0},
                    ),
                ),
                finish=FinishSettings(contrast=1.4, color=1.45),
            ),
            Preset(
                name="Dramatic Black & White",
                steps=(
                    EffectStep(EffectId.GRAYSCALE, {}),
                    EffectStep(EffectId.MIRROR, {"mode": MirrorMode.LEFT.value}),
                ),
                finish=FinishSettings(contrast=1.8, color=1.0),
            ),
            Preset(
                name="Cinema Noir",
                steps=(
                    EffectStep(EffectId.GRAYSCALE, {}),
                    EffectStep(
                        EffectId.WAVE,
                        {"amplitude": 5, "frequency": 1.5, "vertical": False},
                    ),
                ),
                finish=FinishSettings(contrast=1.65, color=1.0),
            ),
            Preset(
                name="Chrome Tunnel",
                steps=(
                    EffectStep(EffectId.MIRROR, {"mode": MirrorMode.TOP.value}),
                    EffectStep(
                        EffectId.PORTAL,
                        {"repetitions": 6, "scale": 0.74, "rotation": 2},
                    ),
                    EffectStep(EffectId.RGB_SPLIT, {"distance": 7}),
                ),
                finish=FinishSettings(contrast=1.45, color=1.2),
            ),
            Preset(
                name="Neon Fracture",
                steps=(
                    EffectStep(EffectId.MIRROR, {"mode": MirrorMode.BOTTOM.value}),
                    EffectStep(EffectId.RGB_SPLIT, {"distance": 38}),
                    EffectStep(
                        EffectId.GLITCH,
                        {"intensity": 54, "block_count": 20, "seed": 9090},
                    ),
                ),
                finish=FinishSettings(contrast=1.3, color=1.85),
            ),
            Preset(
                name="Electric Wave",
                steps=(
                    EffectStep(
                        EffectId.WAVE,
                        {"amplitude": 56, "frequency": 7.0, "vertical": False},
                    ),
                    EffectStep(EffectId.RGB_SPLIT, {"distance": 21}),
                ),
                finish=FinishSettings(contrast=1.2, color=1.75),
            ),
            Preset(
                name="Infinite Reflection",
                steps=(
                    EffectStep(EffectId.MIRROR, {"mode": MirrorMode.LEFT.value}),
                    EffectStep(
                        EffectId.PORTAL,
                        {"repetitions": 10, "scale": 0.82, "rotation": -2},
                    ),
                ),
                finish=FinishSettings(contrast=1.2, color=1.3),
            ),
        )
