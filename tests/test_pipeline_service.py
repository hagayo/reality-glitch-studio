from __future__ import annotations

import pytest
from PIL import Image

from reality_glitch.domain.exceptions import (
    InvalidEffectOutputError,
    InvalidImageError,
    UnknownEffectError,
)
from reality_glitch.domain.models import (
    EffectDefinition,
    EffectId,
    EffectStep,
    FinishSettings,
    PipelineRequest,
)
from reality_glitch.infrastructure.registry import InMemoryEffectRegistry
from reality_glitch.services.image_service import PillowImageService
from reality_glitch.services.pipeline_service import ImagePipelineService


class PixelEffect:
    definition = EffectDefinition(EffectId.WAVE, "Pixel")

    def apply(self, image: Image.Image, settings: dict) -> Image.Image:
        result = image.copy()
        result.putpixel((0, 0), tuple(settings["pixel"]))
        return result

    def settings_for_frame(self, settings: dict, progress: float, frame_index: int) -> dict:
        return dict(settings)


class OrderEffect:
    def __init__(self, effect_id: EffectId, value: int) -> None:
        self.definition = EffectDefinition(effect_id, effect_id.value)
        self._value = value

    def apply(self, image: Image.Image, settings: dict) -> Image.Image:
        result = image.copy()
        previous = result.getpixel((0, 0))[0]
        result.putpixel((0, 0), (previous * 10 + self._value, 0, 0))
        return result

    def settings_for_frame(self, settings: dict, progress: float, frame_index: int) -> dict:
        return dict(settings)


class BadEffect:
    definition = EffectDefinition(EffectId.WAVE, "Bad")

    def apply(self, image: Image.Image, settings: dict):
        return None

    def settings_for_frame(self, settings: dict, progress: float, frame_index: int) -> dict:
        return dict(settings)


def build_service(*effects) -> ImagePipelineService:
    return ImagePipelineService(
        InMemoryEffectRegistry(effects),
        PillowImageService(),
    )


def test_pipeline_depends_on_effect_contract_not_real_effects() -> None:
    service = build_service(PixelEffect())
    image = Image.new("RGB", (2, 2), "black")
    request = PipelineRequest(
        steps=(EffectStep(EffectId.WAVE, {"pixel": (255, 0, 0)}),),
        include_intermediate_steps=True,
    )

    result = service.execute(image, request)

    assert result.image.getpixel((0, 0)) == (255, 0, 0)
    assert len(result.steps) == 1
    assert image.getpixel((0, 0)) == (0, 0, 0)


def test_empty_pipeline_applies_finish_only(rgb_image: Image.Image) -> None:
    service = build_service()

    result = service.execute(
        rgb_image,
        PipelineRequest(steps=(), finish=FinishSettings()),
    )

    assert result.image.size == rgb_image.size
    assert result.steps == ()


def test_pipeline_executes_effects_in_order() -> None:
    service = build_service(
        OrderEffect(EffectId.WAVE, 1),
        OrderEffect(EffectId.GLITCH, 2),
    )
    image = Image.new("RGB", (1, 1), "black")
    request = PipelineRequest(
        steps=(
            EffectStep(EffectId.WAVE),
            EffectStep(EffectId.GLITCH),
        )
    )

    result = service.execute(image, request)

    assert result.image.getpixel((0, 0))[0] == 12


def test_pipeline_omits_intermediate_steps_by_default() -> None:
    service = build_service(PixelEffect())
    request = PipelineRequest(
        steps=(EffectStep(EffectId.WAVE, {"pixel": (1, 2, 3)}),)
    )

    result = service.execute(Image.new("RGB", (1, 1)), request)

    assert result.steps == ()


def test_pipeline_returns_independent_step_images() -> None:
    service = build_service(PixelEffect())
    request = PipelineRequest(
        steps=(EffectStep(EffectId.WAVE, {"pixel": (1, 2, 3)}),),
        include_intermediate_steps=True,
    )

    result = service.execute(Image.new("RGB", (1, 1)), request)
    result.image.putpixel((0, 0), (9, 9, 9))

    assert result.steps[0].image.getpixel((0, 0)) == (1, 2, 3)


def test_pipeline_rejects_non_image_input() -> None:
    service = build_service()

    with pytest.raises(InvalidImageError):
        service.execute("bad", PipelineRequest(steps=()))  # type: ignore[arg-type]


def test_pipeline_reports_unknown_effect() -> None:
    service = build_service()

    with pytest.raises(UnknownEffectError):
        service.execute(
            Image.new("RGB", (1, 1)),
            PipelineRequest(steps=(EffectStep(EffectId.WAVE),)),
        )


def test_pipeline_rejects_invalid_effect_output() -> None:
    service = build_service(BadEffect())

    with pytest.raises(InvalidEffectOutputError, match="did not return"):
        service.execute(
            Image.new("RGB", (1, 1)),
            PipelineRequest(steps=(EffectStep(EffectId.WAVE),)),
        )
