from __future__ import annotations

import pytest
from PIL import Image


@pytest.fixture
def rgb_image() -> Image.Image:
    image = Image.new("RGB", (32, 24), "black")
    for x in range(image.width):
        for y in range(image.height):
            image.putpixel((x, y), ((x * 7) % 256, (y * 11) % 256, (x + y) % 256))
    return image


@pytest.fixture
def tiny_image() -> Image.Image:
    return Image.new("RGB", (1, 1), "white")
