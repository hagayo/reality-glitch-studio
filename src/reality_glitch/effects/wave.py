from __future__ import annotations

import math
from copy import deepcopy
from typing import Any

import numpy as np
from PIL import Image

from reality_glitch.domain.models import EffectDefinition, EffectId
from reality_glitch.effects.base import BaseEffect


class WaveEffect(BaseEffect):
    definition = EffectDefinition(EffectId.WAVE, "גל במציאות")

    def apply(self, image: Image.Image, settings: dict[str, Any]) -> Image.Image:
        amplitude = int(settings.get("amplitude", 25))
        frequency = float(settings.get("frequency", 3.0))
        vertical = bool(settings.get("vertical", False))

        pixels = np.array(image)
        result = np.empty_like(pixels)
        height, width = pixels.shape[:2]

        if vertical:
            for x in range(width):
                angle = 2 * math.pi * frequency * x / max(width, 1)
                result[:, x] = np.roll(
                    pixels[:, x],
                    int(amplitude * math.sin(angle)),
                    axis=0,
                )
        else:
            for y in range(height):
                angle = 2 * math.pi * frequency * y / max(height, 1)
                result[y] = np.roll(
                    pixels[y],
                    int(amplitude * math.sin(angle)),
                    axis=0,
                )

        return Image.fromarray(result)

    def settings_for_frame(
        self,
        settings: dict[str, Any],
        progress: float,
        frame_index: int,
    ) -> dict[str, Any]:
        del frame_index
        frame_settings = deepcopy(settings)
        frame_settings["amplitude"] = round(
            int(frame_settings.get("amplitude", 25)) * progress
        )
        return frame_settings
