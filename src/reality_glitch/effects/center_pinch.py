from __future__ import annotations

from copy import deepcopy
from typing import Any

import numpy as np
from PIL import Image

from reality_glitch.domain.models import EffectDefinition, EffectId
from reality_glitch.effects.base import BaseEffect
from reality_glitch.effects.local_distortion import (
    center_from_percentages,
    normalized_radius_and_angles,
    radius_from_percentage,
    soft_influence,
)
from reality_glitch.effects.sampling import bilinear_sample


class CenterPinchEffect(BaseEffect):
    definition = EffectDefinition(EffectId.CENTER_PINCH, "כיווץ מרכזי")

    def apply(self, image: Image.Image, settings: dict[str, Any]) -> Image.Image:
        strength = float(settings.get("strength", 0.7))
        center_x_pct = float(settings.get("center_x", 50.0))
        center_y_pct = float(settings.get("center_y", 45.0))
        radius_pct = float(settings.get("radius", 32.0))
        falloff = float(settings.get("falloff", 1.8))

        if radius_pct <= 0:
            raise ValueError("radius must be greater than 0")
        if strength == 0:
            return image.copy()

        pixels = np.asarray(image)
        height, width = pixels.shape[:2]
        center_x, center_y = center_from_percentages(width, height, center_x_pct, center_y_pct)
        radius = radius_from_percentage(width, height, radius_pct)
        _, _, _, _, distance, angles = normalized_radius_and_angles(width, height, center_x, center_y)

        influence = soft_influence(distance, radius, falloff)
        scale = 1.0 + (strength * influence)
        source_radius = distance * scale

        source_x = center_x + (source_radius * np.cos(angles))
        source_y = center_y + (source_radius * np.sin(angles))
        outside_mask = distance > radius
        source_x[outside_mask] = center_x + (distance[outside_mask] * np.cos(angles[outside_mask]))
        source_y[outside_mask] = center_y + (distance[outside_mask] * np.sin(angles[outside_mask]))
        return Image.fromarray(bilinear_sample(pixels, source_x, source_y))

    def settings_for_frame(self, settings: dict[str, Any], progress: float, frame_index: int) -> dict[str, Any]:
        del frame_index
        frame_settings = deepcopy(settings)
        frame_settings["strength"] = float(frame_settings.get("strength", 0.7)) * progress
        return frame_settings
