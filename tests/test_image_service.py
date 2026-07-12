from __future__ import annotations

import pytest
from PIL import Image

from reality_glitch.domain.exceptions import InvalidImageError
from reality_glitch.domain.models import FinishSettings
from reality_glitch.services.image_service import PillowImageService


def test_constructor_rejects_non_positive_max_size() -> None:
    with pytest.raises(ValueError, match="positive"):
        PillowImageService(max_size=0)


def test_prepare_rejects_non_image_input() -> None:
    service = PillowImageService()

    with pytest.raises(InvalidImageError, match="Pillow image"):
        service.prepare("not-an-image")  # type: ignore[arg-type]


def test_prepare_converts_rgba_to_rgb() -> None:
    service = PillowImageService()
    image = Image.new("RGBA", (20, 10), (10, 20, 30, 120))

    result = service.prepare(image)

    assert result.mode == "RGB"
    assert result.size == image.size


def test_prepare_converts_grayscale_to_rgb() -> None:
    service = PillowImageService()
    image = Image.new("L", (20, 10), 128)

    result = service.prepare(image)

    assert result.mode == "RGB"


def test_prepare_reduces_large_image_and_keeps_aspect_ratio() -> None:
    service = PillowImageService(max_size=100)
    image = Image.new("RGB", (400, 200), "red")

    result = service.prepare(image)

    assert result.size == (100, 50)


def test_prepare_does_not_upscale_small_image() -> None:
    service = PillowImageService(max_size=100)
    image = Image.new("RGB", (20, 10), "red")

    result = service.prepare(image)

    assert result.size == (20, 10)


def test_prepare_does_not_mutate_original() -> None:
    service = PillowImageService(max_size=10)
    image = Image.new("RGB", (20, 10), "red")

    service.prepare(image)

    assert image.size == (20, 10)


def test_finish_rejects_non_image_input() -> None:
    with pytest.raises(InvalidImageError):
        PillowImageService.finish("bad", FinishSettings())  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "settings",
    [FinishSettings(contrast=-0.1), FinishSettings(color=-0.1)],
)
def test_finish_rejects_negative_values(settings: FinishSettings) -> None:
    with pytest.raises(ValueError, match="non-negative"):
        PillowImageService.finish(Image.new("RGB", (2, 2)), settings)


def test_finish_with_neutral_values_keeps_pixels(rgb_image: Image.Image) -> None:
    result = PillowImageService.finish(rgb_image, FinishSettings())

    assert result.tobytes() == rgb_image.tobytes()
    assert result is not rgb_image
