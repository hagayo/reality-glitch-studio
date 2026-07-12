from __future__ import annotations

from copy import deepcopy
from typing import Any

import numpy as np
from PIL import Image

from reality_glitch.domain.models import EffectDefinition, EffectId
from reality_glitch.effects.base import BaseEffect


class GlitchEffect(BaseEffect):
    definition = EffectDefinition(EffectId.GLITCH, "התפרקות דיגיטלית")

    def apply(self, image: Image.Image, settings: dict[str, Any]) -> Image.Image:
        intensity = max(1, int(settings.get("intensity", 40)))
        block_count = max(1, int(settings.get("block_count", 20)))
        seed = int(settings.get("seed", 42))

        rng = np.random.default_rng(seed)
        pixels = np.array(image)
        result = pixels.copy()
        height, width = pixels.shape[:2]

        if height < 2 or width < 2:
            return image.copy()

        max_block_height = max(2, height // 8)
        for _ in range(block_count):
            block_height = int(rng.integers(2, max_block_height + 1))
            start_y = int(rng.integers(0, max(1, height - block_height + 1)))
            end_y = min(start_y + block_height, height)
            shift = int(rng.integers(-intensity, intensity + 1))
            result[start_y:end_y] = np.roll(
                result[start_y:end_y],
                shift,
                axis=1,
            )

        return Image.fromarray(result)

    def settings_for_frame(
        self,
        settings: dict[str, Any],
        progress: float,
        frame_index: int,
    ) -> dict[str, Any]:
        frame_settings = deepcopy(settings)
        frame_settings["intensity"] = max(
            1,
            round(int(frame_settings.get("intensity", 40)) * progress),
        )
        frame_settings["block_count"] = max(
            1,
            round(int(frame_settings.get("block_count", 20)) * progress),
        )
        frame_settings["seed"] = int(frame_settings.get("seed", 42)) + frame_index
        return frame_settings
