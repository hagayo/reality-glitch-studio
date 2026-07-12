from __future__ import annotations

from copy import deepcopy
from typing import Any

import numpy as np
from PIL import Image

from reality_glitch.domain.models import EffectDefinition, EffectId
from reality_glitch.effects.base import BaseEffect


class DoubleExposureEffect(BaseEffect):
    definition = EffectDefinition(EffectId.DOUBLE_EXPOSURE, "Double Exposure")

    def apply(self, image: Image.Image, settings: dict[str, Any]) -> Image.Image:
        source_image = settings.get("source_image")
        if not isinstance(source_image, Image.Image):
            raise ValueError("Double Exposure requires a source_image")

        opacity = float(settings.get("opacity", 0.45))
        channel_shift = int(settings.get("channel_shift", 8))
        mix_mode = str(settings.get("mix_mode", "screen"))

        if not 0.0 <= opacity <= 1.0:
            raise ValueError("opacity must be between 0 and 1")
        if mix_mode not in {"screen", "add", "blend"}:
            raise ValueError("mix_mode must be screen, add, or blend")

        base = np.asarray(image.convert("RGB"), dtype=np.float32)
        source = source_image.convert("RGB").resize(image.size, Image.Resampling.LANCZOS)
        source_arr = np.asarray(source, dtype=np.float32)

        if channel_shift:
            source_arr[:, :, 0] = np.roll(source_arr[:, :, 0], channel_shift, axis=1)
            source_arr[:, :, 2] = np.roll(source_arr[:, :, 2], -channel_shift, axis=0)

        if mix_mode == "screen":
            blended = 255.0 - ((255.0 - base) * (255.0 - source_arr) / 255.0)
            result = (base * (1.0 - opacity)) + (blended * opacity)
        elif mix_mode == "add":
            result = np.clip(base + (source_arr * opacity), 0.0, 255.0)
        else:
            result = (base * (1.0 - opacity)) + (source_arr * opacity)

        return Image.fromarray(np.clip(result, 0, 255).astype(np.uint8))

    def settings_for_frame(self, settings: dict[str, Any], progress: float, frame_index: int) -> dict[str, Any]:
        del frame_index
        frame_settings = deepcopy(settings)
        frame_settings["opacity"] = float(frame_settings.get("opacity", 0.45)) * progress
        frame_settings["channel_shift"] = round(int(frame_settings.get("channel_shift", 8)) * progress)
        return frame_settings
