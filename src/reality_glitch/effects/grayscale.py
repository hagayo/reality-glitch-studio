from __future__ import annotations

from typing import Any

from PIL import Image, ImageOps

from reality_glitch.domain.models import EffectDefinition, EffectId
from reality_glitch.effects.base import BaseEffect


class GrayscaleEffect(BaseEffect):
    """Convert an image to grayscale while preserving RGB output."""

    definition = EffectDefinition(EffectId.GRAYSCALE, "שחור לבן")

    def apply(self, image: Image.Image, settings: dict[str, Any]) -> Image.Image:
        del settings
        return ImageOps.grayscale(image).convert("RGB")
