from __future__ import annotations

from collections.abc import Iterable
from typing import Any, Protocol

from PIL import Image

from reality_glitch.domain.models import (
    AnimationOptions,
    EffectDefinition,
    EffectId,
    EffectStep,
    PipelineRequest,
    PipelineResult,
    Preset,
)


class ImageEffect(Protocol):
    @property
    def definition(self) -> EffectDefinition: ...

    def apply(self, image: Image.Image, settings: dict[str, Any]) -> Image.Image: ...

    def settings_for_frame(
        self,
        settings: dict[str, Any],
        progress: float,
        frame_index: int,
    ) -> dict[str, Any]: ...


class EffectRegistry(Protocol):
    def get(self, effect_id: EffectId) -> ImageEffect: ...

    def list_definitions(self) -> tuple[EffectDefinition, ...]: ...


class PresetRepository(Protocol):
    def list_all(self) -> tuple[Preset, ...]: ...

    def get(self, name: str) -> Preset: ...


class PipelineProcessor(Protocol):
    def execute(self, image: Image.Image, request: PipelineRequest) -> PipelineResult: ...


class AnimationRenderer(Protocol):
    def render_gif(
        self,
        image: Image.Image,
        request: PipelineRequest,
        options: AnimationOptions,
    ) -> bytes: ...


class ImageExporter(Protocol):
    def to_png(self, image: Image.Image) -> bytes: ...
