from __future__ import annotations

from copy import deepcopy
from typing import Any

import numpy as np
from PIL import Image

from reality_glitch.domain.models import EffectDefinition, EffectId
from reality_glitch.effects.base import BaseEffect
from reality_glitch.effects.sampling import bilinear_sample


class CircularRippleEffect(BaseEffect):
    definition = EffectDefinition(EffectId.CIRCULAR_RIPPLE, "גלים מעגליים")

    def apply(self, image: Image.Image, settings: dict[str, Any]) -> Image.Image:
        amplitude = int(settings.get("amplitude", 18))
        wavelength = int(settings.get("wavelength", 40))
        phase_degrees = float(settings.get("phase_degrees", 0.0))

        if wavelength <= 0:
            raise ValueError("wavelength must be greater than 0")
        if amplitude == 0:
            return image.copy()

        pixels = np.asarray(image)
        height, width = pixels.shape[:2]
        center_x = (width - 1) / 2.0
        center_y = (height - 1) / 2.0

        grid_y, grid_x = np.indices((height, width), dtype=float)
        delta_x = grid_x - center_x
        delta_y = grid_y - center_y

        radius = np.sqrt((delta_x**2) + (delta_y**2))
        angles = np.arctan2(delta_y, delta_x)
        phase = np.deg2rad(phase_degrees)

        displaced_radius = radius + (
            amplitude * np.sin(((2.0 * np.pi * radius) / wavelength) + phase)
        )

        source_x = center_x + (displaced_radius * np.cos(angles))
        source_y = center_y + (displaced_radius * np.sin(angles))

        return Image.fromarray(bilinear_sample(pixels, source_x, source_y))

    def settings_for_frame(
        self,
        settings: dict[str, Any],
        progress: float,
        frame_index: int,
    ) -> dict[str, Any]:
        frame_settings = deepcopy(settings)
        frame_settings["amplitude"] = round(
            int(frame_settings.get("amplitude", 18)) * progress
        )
        frame_settings["phase_degrees"] = (
            float(frame_settings.get("phase_degrees", 0.0)) + (frame_index * 18)
        )
        return frame_settings
