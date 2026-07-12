from __future__ import annotations

from copy import deepcopy
from typing import Any

import numpy as np
from PIL import Image

from reality_glitch.domain.models import EffectDefinition, EffectId
from reality_glitch.effects.base import BaseEffect
from reality_glitch.effects.sampling import bilinear_sample


class SwirlEffect(BaseEffect):
    definition = EffectDefinition(EffectId.SWIRL, "סחרור")

    def apply(self, image: Image.Image, settings: dict[str, Any]) -> Image.Image:
        strength = float(settings.get("strength", 3.5))
        radius = float(settings.get("radius", min(image.size) / 2.0))

        if radius <= 0:
            raise ValueError("radius must be greater than 0")
        if strength == 0:
            return image.copy()

        pixels = np.asarray(image)
        height, width = pixels.shape[:2]
        center_x = (width - 1) / 2.0
        center_y = (height - 1) / 2.0

        grid_y, grid_x = np.indices((height, width), dtype=float)
        delta_x = grid_x - center_x
        delta_y = grid_y - center_y

        distance = np.sqrt((delta_x ** 2) + (delta_y ** 2))
        angles = np.arctan2(delta_y, delta_x)

        influence = np.clip((radius - distance) / radius, 0.0, 1.0)
        twisted_angles = angles + (strength * influence)

        source_x = center_x + (distance * np.cos(twisted_angles))
        source_y = center_y + (distance * np.sin(twisted_angles))

        return Image.fromarray(bilinear_sample(pixels, source_x, source_y))

    def settings_for_frame(
        self,
        settings: dict[str, Any],
        progress: float,
        frame_index: int,
    ) -> dict[str, Any]:
        del frame_index
        frame_settings = deepcopy(settings)
        frame_settings["strength"] = float(frame_settings.get("strength", 3.5)) * progress
        return frame_settings
