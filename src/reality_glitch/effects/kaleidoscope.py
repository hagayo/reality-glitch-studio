from __future__ import annotations

from copy import deepcopy
from typing import Any

import numpy as np
from PIL import Image

from reality_glitch.domain.models import EffectDefinition, EffectId
from reality_glitch.effects.base import BaseEffect
from reality_glitch.effects.sampling import bilinear_sample


class KaleidoscopeEffect(BaseEffect):
    definition = EffectDefinition(EffectId.KALEIDOSCOPE, "קליידוסקופ")

    def apply(self, image: Image.Image, settings: dict[str, Any]) -> Image.Image:
        segments = int(settings.get("segments", 6))
        rotation_degrees = float(settings.get("rotation_degrees", 0.0))
        zoom = float(settings.get("zoom", 1.0))

        if segments < 2:
            raise ValueError("segments must be at least 2")
        if zoom <= 0:
            raise ValueError("zoom must be greater than 0")

        pixels = np.asarray(image)
        height, width = pixels.shape[:2]
        center_x = (width - 1) / 2.0
        center_y = (height - 1) / 2.0

        grid_y, grid_x = np.indices((height, width), dtype=float)
        delta_x = (grid_x - center_x) / zoom
        delta_y = (grid_y - center_y) / zoom

        radius = np.sqrt((delta_x**2) + (delta_y**2))
        angles = np.arctan2(delta_y, delta_x) + np.deg2rad(rotation_degrees)

        sector = (2.0 * np.pi) / segments
        folded = np.mod(angles, sector)
        folded = np.where(folded > (sector / 2.0), sector - folded, folded)

        source_x = center_x + (radius * np.cos(folded))
        source_y = center_y + (radius * np.sin(folded))

        return Image.fromarray(bilinear_sample(pixels, source_x, source_y))

    def settings_for_frame(
        self,
        settings: dict[str, Any],
        progress: float,
        frame_index: int,
    ) -> dict[str, Any]:
        del frame_index
        frame_settings = deepcopy(settings)
        frame_settings["rotation_degrees"] = (
            float(frame_settings.get("rotation_degrees", 0.0)) * progress
        )
        return frame_settings
