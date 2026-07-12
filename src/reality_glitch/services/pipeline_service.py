from __future__ import annotations

from PIL import Image

from reality_glitch.domain.exceptions import InvalidEffectOutputError, InvalidImageError
from reality_glitch.domain.models import (
    PipelineRequest,
    PipelineResult,
    PipelineStepResult,
)
from reality_glitch.domain.ports import EffectRegistry
from reality_glitch.services.image_service import PillowImageService
from reality_glitch.services.mask_service import build_mask_image


class ImagePipelineService:
    """Execute registered effects in order and apply final image adjustments."""

    def __init__(
        self,
        registry: EffectRegistry,
        image_service: PillowImageService,
    ) -> None:
        self._registry = registry
        self._image_service = image_service

    def execute(
        self,
        image: Image.Image,
        request: PipelineRequest,
    ) -> PipelineResult:
        if not isinstance(image, Image.Image):
            raise InvalidImageError("Pipeline input must be a Pillow image")

        result = image.copy()
        step_results: list[PipelineStepResult] = []

        for step in request.steps:
            effect = self._registry.get(step.effect_id)
            next_result = effect.apply(result, dict(step.settings))

            if not isinstance(next_result, Image.Image):
                raise InvalidEffectOutputError(
                    f"Effect {step.effect_id} did not return a Pillow image"
                )

            if step.mask:
                mask_image = build_mask_image(result.size, step.mask)
                if mask_image is not None:
                    next_result = Image.composite(next_result, result, mask_image)

            result = next_result
            if request.include_intermediate_steps:
                step_results.append(
                    PipelineStepResult(step.effect_id, result.copy())
                )

        result = self._image_service.finish(result, request.finish)
        return PipelineResult(result, tuple(step_results))
