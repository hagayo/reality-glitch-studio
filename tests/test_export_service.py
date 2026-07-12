from __future__ import annotations

from io import BytesIO

from PIL import Image

from reality_glitch.services.export_service import PillowImageExporter


def test_export_returns_valid_png(rgb_image: Image.Image) -> None:
    data = PillowImageExporter.to_png(rgb_image)

    assert data.startswith(b"\x89PNG\r\n\x1a\n")
    reopened = Image.open(BytesIO(data))
    assert reopened.size == rgb_image.size
    assert reopened.mode == "RGB"


def test_export_preserves_rgba_mode() -> None:
    image = Image.new("RGBA", (3, 2), (1, 2, 3, 4))

    data = PillowImageExporter.to_png(image)
    reopened = Image.open(BytesIO(data))

    assert reopened.mode == "RGBA"
    assert reopened.getpixel((0, 0)) == (1, 2, 3, 4)
