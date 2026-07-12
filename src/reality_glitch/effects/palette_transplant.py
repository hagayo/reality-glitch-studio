from __future__ import annotations

from copy import deepcopy
from typing import Any

import numpy as np
from PIL import Image

from reality_glitch.domain.models import EffectDefinition, EffectId
from reality_glitch.effects.base import BaseEffect


class PaletteTransplantEffect(BaseEffect):
    definition = EffectDefinition(EffectId.PALETTE_TRANSPLANT, "Palette Transplant")

    def apply(self, image: Image.Image, settings: dict[str, Any]) -> Image.Image:
        palette_image = settings.get("palette_image")
        if not isinstance(palette_image, Image.Image):
            raise ValueError("Palette Transplant requires a palette_image")

        contrast = float(settings.get("gradient_contrast", 1.0))
        mode = str(settings.get("mode", "gradient"))
        if contrast <= 0:
            raise ValueError("gradient_contrast must be greater than 0")
        if mode not in {"gradient", "duotone"}:
            raise ValueError("mode must be gradient or duotone")

        palette_source = palette_image.convert("RGB").resize((160, 160), Image.Resampling.LANCZOS)
        quantized = palette_source.quantize(colors=5, method=Image.Quantize.MEDIANCUT).convert("RGB")
        colors = np.asarray(quantized, dtype=np.uint8).reshape(-1, 3)
        unique, counts = np.unique(colors, axis=0, return_counts=True)
        ranked = unique[np.argsort(counts)[::-1]]
        brightness = ranked @ np.array([0.299, 0.587, 0.114])
        ranked = ranked[np.argsort(brightness)]

        base = np.asarray(image.convert("RGB"), dtype=np.float32)
        luminance = ((base[:, :, 0] * 0.299) + (base[:, :, 1] * 0.587) + (base[:, :, 2] * 0.114)) / 255.0
        midpoint = np.clip(((luminance - 0.5) * contrast) + 0.5, 0.0, 1.0)

        if mode == "duotone":
            low = ranked[0].astype(np.float32)
            high = ranked[-1].astype(np.float32)
            mapped = low + ((high - low) * midpoint[..., None])
        else:
            if len(ranked) < 2:
                ranked = np.vstack([ranked, ranked])
            anchors = np.linspace(0.0, 1.0, len(ranked))
            mapped = np.empty((*midpoint.shape, 3), dtype=np.float32)
            for channel in range(3):
                mapped[:, :, channel] = np.interp(midpoint, anchors, ranked[:, channel])

        return Image.fromarray(np.clip(mapped, 0, 255).astype(np.uint8))

    def settings_for_frame(self, settings: dict[str, Any], progress: float, frame_index: int) -> dict[str, Any]:
        del frame_index
        frame_settings = deepcopy(settings)
        target = float(frame_settings.get("gradient_contrast", 1.0))
        frame_settings["gradient_contrast"] = 1.0 + ((target - 1.0) * progress)
        return frame_settings
