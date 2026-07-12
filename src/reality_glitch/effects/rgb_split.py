from __future__ import annotations

from copy import deepcopy
from typing import Any

import numpy as np
from PIL import Image

from reality_glitch.domain.models import EffectDefinition, EffectId
from reality_glitch.effects.base import BaseEffect


class RgbSplitEffect(BaseEffect):
    definition = EffectDefinition(EffectId.RGB_SPLIT, "הפרדת צבעים")

    def apply(self, image: Image.Image, settings: dict[str, Any]) -> Image.Image:
        distance = int(settings.get("distance", 15))
        pixels = np.array(image)
        result = np.zeros_like(pixels)
        result[:, :, 0] = np.roll(pixels[:, :, 0], distance, axis=1)
        result[:, :, 1] = pixels[:, :, 1]
        result[:, :, 2] = np.roll(pixels[:, :, 2], -distance, axis=1)
        return Image.fromarray(result)

    def settings_for_frame(
        self,
        settings: dict[str, Any],
        progress: float,
        frame_index: int,
    ) -> dict[str, Any]:
        del frame_index
        frame_settings = deepcopy(settings)
        frame_settings["distance"] = round(
            int(frame_settings.get("distance", 15)) * progress
        )
        return frame_settings
