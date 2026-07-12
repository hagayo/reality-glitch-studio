from __future__ import annotations

from typing import Any

import numpy as np
from PIL import Image

from reality_glitch.domain.models import EffectDefinition, EffectId, MirrorMode
from reality_glitch.effects.base import BaseEffect


class MirrorEffect(BaseEffect):
    definition = EffectDefinition(EffectId.MIRROR, "מראה בלתי אפשרית")

    def apply(self, image: Image.Image, settings: dict[str, Any]) -> Image.Image:
        mode = MirrorMode(settings.get("mode", MirrorMode.LEFT.value))
        pixels = np.array(image)
        height, width = pixels.shape[:2]
        result = pixels.copy()
        middle_x = width // 2
        middle_y = height // 2

        if mode is MirrorMode.LEFT:
            mirrored = np.flip(pixels[:, :middle_x], axis=1)
            result[:, width - mirrored.shape[1] :] = mirrored
        elif mode is MirrorMode.RIGHT:
            mirrored = np.flip(pixels[:, width - middle_x :], axis=1)
            result[:, : mirrored.shape[1]] = mirrored
        elif mode is MirrorMode.TOP:
            mirrored = np.flip(pixels[:middle_y], axis=0)
            result[height - mirrored.shape[0] :] = mirrored
        else:
            mirrored = np.flip(pixels[height - middle_y :], axis=0)
            result[: mirrored.shape[0]] = mirrored

        return Image.fromarray(result)
