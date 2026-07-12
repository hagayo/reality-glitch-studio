from __future__ import annotations

from copy import deepcopy
from typing import Any

import numpy as np
from PIL import Image

from reality_glitch.domain.models import EffectDefinition, EffectId
from reality_glitch.effects.base import BaseEffect


class PixelSortEffect(BaseEffect):
    definition = EffectDefinition(EffectId.PIXEL_SORT, "מיון פיקסלים")

    def apply(self, image: Image.Image, settings: dict[str, Any]) -> Image.Image:
        orientation = str(settings.get("orientation", "horizontal"))
        threshold = int(settings.get("threshold", 110))
        reverse = bool(settings.get("reverse", False))
        min_segment_length = max(1, int(settings.get("min_segment_length", 8)))

        if orientation not in {"horizontal", "vertical"}:
            raise ValueError("orientation must be 'horizontal' or 'vertical'")

        pixels = np.asarray(image)
        result = pixels.copy()
        luminance = self._compute_luminance(pixels)

        if orientation == "horizontal":
            for row_index in range(result.shape[0]):
                result[row_index] = self._sort_line(
                    result[row_index],
                    luminance[row_index],
                    threshold,
                    reverse,
                    min_segment_length,
                )
        else:
            for column_index in range(result.shape[1]):
                result[:, column_index] = self._sort_line(
                    result[:, column_index],
                    luminance[:, column_index],
                    threshold,
                    reverse,
                    min_segment_length,
                )

        return Image.fromarray(result)

    def settings_for_frame(
        self,
        settings: dict[str, Any],
        progress: float,
        frame_index: int,
    ) -> dict[str, Any]:
        del frame_index
        frame_settings = deepcopy(settings)
        target_threshold = int(frame_settings.get("threshold", 110))
        frame_settings["threshold"] = round(
            255 - ((255 - target_threshold) * progress)
        )
        return frame_settings

    @staticmethod
    def _compute_luminance(pixels: np.ndarray) -> np.ndarray:
        return (
            (0.299 * pixels[:, :, 0])
            + (0.587 * pixels[:, :, 1])
            + (0.114 * pixels[:, :, 2])
        )

    def _sort_line(
        self,
        line_pixels: np.ndarray,
        line_luminance: np.ndarray,
        threshold: int,
        reverse: bool,
        min_segment_length: int,
    ) -> np.ndarray:
        line_result = line_pixels.copy()
        mask = line_luminance >= threshold
        start_index: int | None = None

        for index, is_selected in enumerate(mask):
            if is_selected and start_index is None:
                start_index = index
            elif not is_selected and start_index is not None:
                self._sort_segment(
                    line_result,
                    line_luminance,
                    start_index,
                    index,
                    reverse,
                    min_segment_length,
                )
                start_index = None

        if start_index is not None:
            self._sort_segment(
                line_result,
                line_luminance,
                start_index,
                len(mask),
                reverse,
                min_segment_length,
            )

        return line_result

    @staticmethod
    def _sort_segment(
        line_pixels: np.ndarray,
        line_luminance: np.ndarray,
        start_index: int,
        end_index: int,
        reverse: bool,
        min_segment_length: int,
    ) -> None:
        if (end_index - start_index) < min_segment_length:
            return

        segment_pixels = line_pixels[start_index:end_index]
        segment_luminance = line_luminance[start_index:end_index]
        sorted_indices = np.argsort(segment_luminance, kind="stable")
        if reverse:
            sorted_indices = sorted_indices[::-1]
        line_pixels[start_index:end_index] = segment_pixels[sorted_indices]
