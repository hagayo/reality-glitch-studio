from __future__ import annotations

from copy import deepcopy
from typing import Any

import numpy as np
from PIL import Image

from reality_glitch.domain.models import EffectDefinition, EffectId
from reality_glitch.effects.base import BaseEffect


class RetroCrtEffect(BaseEffect):
    definition = EffectDefinition(EffectId.RETRO_CRT, "מסך CRT")

    def apply(self, image: Image.Image, settings: dict[str, Any]) -> Image.Image:
        scanline_strength = float(settings.get("scanline_strength", 0.22))
        line_spacing = int(settings.get("line_spacing", 3))
        channel_shift = int(settings.get("channel_shift", 2))
        noise_strength = float(settings.get("noise_strength", 0.02))
        seed = int(settings.get("seed", 42))

        if line_spacing <= 0:
            raise ValueError("line_spacing must be greater than 0")
        if scanline_strength < 0 or noise_strength < 0:
            raise ValueError("strength values must be non-negative")

        rng = np.random.default_rng(seed)
        pixels = np.asarray(image).astype(np.float32)
        result = pixels.copy()
        height, width = result.shape[:2]

        if channel_shift:
            result[:, :, 0] = np.roll(result[:, :, 0], channel_shift, axis=1)
            result[:, :, 2] = np.roll(result[:, :, 2], -channel_shift, axis=1)

        scanline_mask = np.ones((height, 1, 1), dtype=np.float32)
        dark_rows = (np.arange(height) % line_spacing) == 0
        scanline_mask[dark_rows] = max(0.0, 1.0 - scanline_strength)
        result *= scanline_mask

        center_x = (width - 1) / 2.0
        center_y = (height - 1) / 2.0
        grid_y, grid_x = np.indices((height, width), dtype=np.float32)
        distance = np.sqrt(((grid_x - center_x) / max(width, 1)) ** 2 + ((grid_y - center_y) / max(height, 1)) ** 2)
        vignette = np.clip(1.15 - (distance * 1.8), 0.7, 1.15)
        result *= vignette[..., None]

        if noise_strength > 0:
            noise = rng.normal(0.0, 255.0 * noise_strength, size=result.shape)
            result += noise

        return Image.fromarray(np.clip(result, 0, 255).astype(np.uint8))

    def settings_for_frame(
        self,
        settings: dict[str, Any],
        progress: float,
        frame_index: int,
    ) -> dict[str, Any]:
        frame_settings = deepcopy(settings)
        frame_settings["scanline_strength"] = (
            float(frame_settings.get("scanline_strength", 0.22)) * progress
        )
        frame_settings["noise_strength"] = (
            float(frame_settings.get("noise_strength", 0.02)) * progress
        )
        frame_settings["seed"] = int(frame_settings.get("seed", 42)) + frame_index
        return frame_settings
