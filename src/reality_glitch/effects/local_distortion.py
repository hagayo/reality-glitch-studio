from __future__ import annotations

import numpy as np


def center_from_percentages(width: int, height: int, center_x: float, center_y: float) -> tuple[float, float]:
    x = ((width - 1) * center_x) / 100.0
    y = ((height - 1) * center_y) / 100.0
    return x, y


def radius_from_percentage(width: int, height: int, radius_percent: float) -> float:
    shortest_side = max(1.0, float(min(width, height)))
    return max(1.0, shortest_side * (radius_percent / 100.0))


def normalized_radius_and_angles(
    width: int,
    height: int,
    center_x: float,
    center_y: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    grid_y, grid_x = np.indices((height, width), dtype=float)
    delta_x = grid_x - center_x
    delta_y = grid_y - center_y
    distance = np.sqrt((delta_x ** 2) + (delta_y ** 2))
    angles = np.arctan2(delta_y, delta_x)
    return grid_x, grid_y, delta_x, delta_y, distance, angles


def soft_influence(distance: np.ndarray, radius: float, falloff: float) -> np.ndarray:
    normalized = np.clip(distance / max(radius, 1e-6), 0.0, 1.0)
    influence = np.clip(1.0 - normalized, 0.0, 1.0)
    return influence ** max(falloff, 0.1)
