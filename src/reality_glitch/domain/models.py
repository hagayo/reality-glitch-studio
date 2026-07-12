from __future__ import annotations

from dataclasses import dataclass, field, replace
from enum import StrEnum
from typing import Any


class EffectId(StrEnum):
    WAVE = "wave"
    GLITCH = "glitch"
    RGB_SPLIT = "rgb_split"
    MIRROR = "mirror"
    PORTAL = "portal"
    GRAYSCALE = "grayscale"
    PIXEL_SORT = "pixel_sort"
    KALEIDOSCOPE = "kaleidoscope"
    CIRCULAR_RIPPLE = "circular_ripple"
    MOSAIC = "mosaic"
    SWIRL = "swirl"
    RETRO_CRT = "retro_crt"
    CENTER_BULGE = "center_bulge"
    CENTER_PINCH = "center_pinch"
    LOCAL_TWIRL = "local_twirl"
    DOUBLE_EXPOSURE = "double_exposure"
    PALETTE_TRANSPLANT = "palette_transplant"


class MirrorMode(StrEnum):
    LEFT = "left"
    RIGHT = "right"
    TOP = "top"
    BOTTOM = "bottom"


@dataclass(frozen=True, slots=True)
class EffectDefinition:
    effect_id: EffectId
    display_name: str


@dataclass(frozen=True, slots=True)
class EffectStep:
    effect_id: EffectId
    settings: dict[str, Any] = field(default_factory=dict)
    mask: dict[str, Any] | None = None

    def with_settings(self, **changes: Any) -> EffectStep:
        return replace(self, settings={**self.settings, **changes})


@dataclass(frozen=True, slots=True)
class FinishSettings:
    contrast: float = 1.0
    color: float = 1.0


@dataclass(frozen=True, slots=True)
class PipelineRequest:
    steps: tuple[EffectStep, ...]
    finish: FinishSettings = FinishSettings()
    include_intermediate_steps: bool = False


@dataclass(frozen=True, slots=True)
class PipelineStepResult:
    effect_id: EffectId
    image: Any


@dataclass(frozen=True, slots=True)
class PipelineResult:
    image: Any
    steps: tuple[PipelineStepResult, ...] = ()


@dataclass(frozen=True, slots=True)
class Preset:
    name: str
    steps: tuple[EffectStep, ...]
    finish: FinishSettings


@dataclass(frozen=True, slots=True)
class AnimationOptions:
    frame_count: int = 12
    frame_duration_ms: int = 90
    ping_pong: bool = True
    mode: str = "ping_pong"
    animated_step_index: int = 0
    animated_parameter: str = ""
    parameter_swing: float = 0.35
    waveform: str = "sine"

    def __post_init__(self) -> None:
        if self.frame_count < 2:
            raise ValueError("frame_count must be at least 2")
        if self.frame_duration_ms < 20:
            raise ValueError("frame_duration_ms must be at least 20")
        if self.mode not in {"ping_pong", "build_up", "parameter"}:
            raise ValueError("mode must be ping_pong, build_up, or parameter")
        if self.parameter_swing < 0:
            raise ValueError("parameter_swing must be non-negative")
        if self.waveform not in {"sine"}:
            raise ValueError("waveform must be sine")
