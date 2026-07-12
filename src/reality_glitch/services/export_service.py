from __future__ import annotations

from io import BytesIO

from PIL import Image


class PillowImageExporter:
    @staticmethod
    def to_png(image: Image.Image) -> bytes:
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        return buffer.getvalue()
