from __future__ import annotations

from copy import deepcopy
from typing import Any

from PIL import Image

from reality_glitch.domain.models import EffectDefinition, EffectId
from reality_glitch.effects.base import BaseEffect


class PortalEffect(BaseEffect):
    definition = EffectDefinition(EffectId.PORTAL, "פורטל אינסופי")

    def apply(self, image: Image.Image, settings: dict[str, Any]) -> Image.Image:
        repetitions = int(settings.get("repetitions", 6))
        scale = float(settings.get("scale", 0.72))
        rotation = int(settings.get("rotation", 4))

        if repetitions < 0:
            raise ValueError("repetitions must be non-negative")
        if not 0 < scale < 1:
            raise ValueError("scale must be between 0 and 1")

        result = image.copy()
        canvas_width, canvas_height = result.size
        current_width, current_height = result.size

        for index in range(1, repetitions + 1):
            current_width = int(current_width * scale)
            current_height = int(current_height * scale)
            if current_width < 10 or current_height < 10:
                break

            smaller = image.resize(
                (current_width, current_height),
                Image.Resampling.LANCZOS,
            )
            if rotation:
                smaller = smaller.rotate(
                    rotation * index,
                    resample=Image.Resampling.BICUBIC,
                    expand=True,
                )

            result.paste(
                smaller,
                (
                    (canvas_width - smaller.width) // 2,
                    (canvas_height - smaller.height) // 2,
                ),
            )

        return result

    def settings_for_frame(
        self,
        settings: dict[str, Any],
        progress: float,
        frame_index: int,
    ) -> dict[str, Any]:
        del frame_index
        frame_settings = deepcopy(settings)
        frame_settings["repetitions"] = max(
            0,
            round(int(frame_settings.get("repetitions", 6)) * progress),
        )
        frame_settings["rotation"] = round(
            int(frame_settings.get("rotation", 4)) * progress
        )
        return frame_settings
