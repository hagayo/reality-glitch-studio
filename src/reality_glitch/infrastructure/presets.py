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
            Preset(
                name="Sorted Spectrum",
                steps=(
                    EffectStep(
                        EffectId.PIXEL_SORT,
                        {"orientation": "horizontal", "threshold": 96, "reverse": False, "min_segment_length": 10},
                    ),
                    EffectStep(EffectId.RGB_SPLIT, {"distance": 14}),
                ),
                finish=FinishSettings(contrast=1.15, color=1.55),
            ),
            Preset(
                name="Crystal Bloom",
                steps=(
                    EffectStep(
                        EffectId.KALEIDOSCOPE,
                        {"segments": 8, "rotation_degrees": 18.0, "zoom": 1.0},
                    ),
                    EffectStep(EffectId.RGB_SPLIT, {"distance": 10}),
                ),
                finish=FinishSettings(contrast=1.18, color=1.35),
            ),
            Preset(
                name="Ripple Dream",
                steps=(
                    EffectStep(
                        EffectId.CIRCULAR_RIPPLE,
                        {"amplitude": 18, "wavelength": 34, "phase_degrees": 0.0},
                    ),
                    EffectStep(
                        EffectId.WAVE,
                        {"amplitude": 10, "frequency": 2.0, "vertical": False},
                    ),
                ),
                finish=FinishSettings(contrast=1.05, color=1.25),
            ),
            Preset(
                name="Prism Storm",
                steps=(
                    EffectStep(
                        EffectId.CIRCULAR_RIPPLE,
                        {"amplitude": 14, "wavelength": 28, "phase_degrees": 45.0},
                    ),
                    EffectStep(
                        EffectId.KALEIDOSCOPE,
                        {"segments": 6, "rotation_degrees": 12.0, "zoom": 0.95},
                    ),
                    EffectStep(
                        EffectId.PIXEL_SORT,
                        {"orientation": "vertical", "threshold": 120, "reverse": True, "min_segment_length": 12},
                    ),
                ),
                finish=FinishSettings(contrast=1.22, color=1.6),
            ),
            Preset(
                name="Aurora Bloom",
                steps=(
                    EffectStep(
                        EffectId.KALEIDOSCOPE,
                        {"segments": 10, "rotation_degrees": 24.0, "zoom": 1.08},
                    ),
                    EffectStep(
                        EffectId.CIRCULAR_RIPPLE,
                        {"amplitude": 10, "wavelength": 42, "phase_degrees": 10.0},
                    ),
                    EffectStep(EffectId.RGB_SPLIT, {"distance": 8}),
                ),
                finish=FinishSettings(contrast=1.12, color=1.55),
            ),
            Preset(
                name="Melted Skyline",
                steps=(
                    EffectStep(
                        EffectId.PIXEL_SORT,
                        {"orientation": "vertical", "threshold": 88, "reverse": False, "min_segment_length": 9},
                    ),
                    EffectStep(
                        EffectId.WAVE,
                        {"amplitude": 16, "frequency": 2.5, "vertical": True},
                    ),
                ),
                finish=FinishSettings(contrast=1.18, color=1.35),
            ),
            Preset(
                name="Noir Spiral",
                steps=(
                    EffectStep(EffectId.GRAYSCALE, {}),
                    EffectStep(
                        EffectId.KALEIDOSCOPE,
                        {"segments": 7, "rotation_degrees": 14.0, "zoom": 1.0},
                    ),
                ),
                finish=FinishSettings(contrast=1.7, color=1.0),
            ),
            Preset(
                name="Glass Echo",
                steps=(
                    EffectStep(EffectId.MIRROR, {"mode": MirrorMode.TOP.value}),
                    EffectStep(
                        EffectId.KALEIDOSCOPE,
                        {"segments": 6, "rotation_degrees": 8.0, "zoom": 0.9},
                    ),
                    EffectStep(
                        EffectId.PORTAL,
                        {"repetitions": 4, "scale": 0.76, "rotation": 0},
                    ),
                ),
                finish=FinishSettings(contrast=1.28, color=1.3),
            ),
            Preset(
                name="Static Tide",
                steps=(
                    EffectStep(
                        EffectId.CIRCULAR_RIPPLE,
                        {"amplitude": 12, "wavelength": 24, "phase_degrees": 0.0},
                    ),
                    EffectStep(
                        EffectId.GLITCH,
                        {"intensity": 34, "block_count": 14, "seed": 5151},
                    ),
                ),
                finish=FinishSettings(contrast=1.14, color=1.4),
            ),
            Preset(
                name="Mosaic Pop",
                steps=(
                    EffectStep(EffectId.MOSAIC, {"block_size": 14}),
                    EffectStep(EffectId.RGB_SPLIT, {"distance": 9}),
                ),
                finish=FinishSettings(contrast=1.1, color=1.35),
            ),
            Preset(
                name="Twisted Center",
                steps=(
                    EffectStep(EffectId.SWIRL, {"strength": 4.8, "radius": 210.0}),
                    EffectStep(EffectId.CIRCULAR_RIPPLE, {"amplitude": 10, "wavelength": 36, "phase_degrees": 0.0}),
                ),
                finish=FinishSettings(contrast=1.12, color=1.25),
            ),
            Preset(
                name="Retro Broadcast",
                steps=(
                    EffectStep(EffectId.RETRO_CRT, {"scanline_strength": 0.28, "line_spacing": 3, "channel_shift": 2, "noise_strength": 0.03, "seed": 1984}),
                    EffectStep(EffectId.GLITCH, {"intensity": 18, "block_count": 8, "seed": 202}),
                ),
                finish=FinishSettings(contrast=1.05, color=1.1),
            ),
            Preset(
                name="Retro Mosaic",
                steps=(
                    EffectStep(EffectId.MOSAIC, {"block_size": 18}),
                    EffectStep(EffectId.RETRO_CRT, {"scanline_strength": 0.18, "line_spacing": 4, "channel_shift": 1, "noise_strength": 0.015, "seed": 77}),
                ),
                finish=FinishSettings(contrast=1.08, color=1.2),
            ),
            Preset(
                name="Vortex Bloom",
                steps=(
                    EffectStep(EffectId.SWIRL, {"strength": 6.0, "radius": 240.0}),
                    EffectStep(EffectId.KALEIDOSCOPE, {"segments": 8, "rotation_degrees": 14.0, "zoom": 1.05}),
                ),
                finish=FinishSettings(contrast=1.18, color=1.5),
            ),
        )
