from __future__ import annotations

import numpy as np


def bilinear_sample(pixels: np.ndarray, source_x: np.ndarray, source_y: np.ndarray) -> np.ndarray:
    """Sample an RGB image using bilinear interpolation."""
    height, width = pixels.shape[:2]

    x0 = np.floor(source_x).astype(int)
    y0 = np.floor(source_y).astype(int)
    x1 = np.clip(x0 + 1, 0, width - 1)
    y1 = np.clip(y0 + 1, 0, height - 1)

    x0 = np.clip(x0, 0, width - 1)
    y0 = np.clip(y0, 0, height - 1)

    dx = (source_x - x0)[..., None]
    dy = (source_y - y0)[..., None]

    top_left = pixels[y0, x0].astype(float)
    top_right = pixels[y0, x1].astype(float)
    bottom_left = pixels[y1, x0].astype(float)
    bottom_right = pixels[y1, x1].astype(float)

    top = top_left * (1.0 - dx) + top_right * dx
    bottom = bottom_left * (1.0 - dx) + bottom_right * dx
    result = top * (1.0 - dy) + bottom * dy

    return np.clip(result, 0, 255).astype(np.uint8)
