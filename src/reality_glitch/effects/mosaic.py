from __future__ import annotations

from copy import deepcopy
from typing import Any

from PIL import Image

from reality_glitch.domain.models import EffectDefinition, EffectId
from reality_glitch.effects.base import BaseEffect


class MosaicEffect(BaseEffect):
    definition = EffectDefinition(EffectId.MOSAIC, "פסיפס")

    def apply(self, image: Image.Image, settings: dict[str, Any]) -> Image.Image:
        block_size = int(settings.get("block_size", 12))
        if block_size <= 0:
            raise ValueError("block_size must be greater than 0")

        width, height = image.size
        down_width = max(1, round(width / block_size))
        down_height = max(1, round(height / block_size))

        reduced = image.resize((down_width, down_height), Image.Resampling.BILINEAR)
        return reduced.resize((width, height), Image.Resampling.NEAREST)

    def settings_for_frame(
        self,
        settings: dict[str, Any],
        progress: float,
        frame_index: int,
    ) -> dict[str, Any]:
        del frame_index
        frame_settings = deepcopy(settings)
        target = int(frame_settings.get("block_size", 12))
        frame_settings["block_size"] = max(1, round(1 + ((target - 1) * progress)))
        return frame_settings
