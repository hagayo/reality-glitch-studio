from __future__ import annotations

from PIL import Image, ImageEnhance, ImageOps, UnidentifiedImageError

from reality_glitch.domain.exceptions import InvalidImageError
from reality_glitch.domain.models import FinishSettings


class PillowImageService:
    """Prepare uploaded images and apply non-destructive finishing adjustments."""

    def __init__(self, max_size: int = 1200) -> None:
        if max_size < 1:
            raise ValueError("max_size must be positive")
        self._max_size = max_size

    def prepare(self, image: Image.Image) -> Image.Image:
        if not isinstance(image, Image.Image):
            raise InvalidImageError("Input must be a Pillow image")

        try:
            prepared = ImageOps.exif_transpose(image).convert("RGB")
            prepared.thumbnail((self._max_size, self._max_size))
            return prepared
        except (UnidentifiedImageError, OSError, ValueError) as error:
            raise InvalidImageError("Could not prepare the uploaded image") from error

    @staticmethod
    def finish(image: Image.Image, settings: FinishSettings) -> Image.Image:
        if not isinstance(image, Image.Image):
            raise InvalidImageError("Input must be a Pillow image")
        if settings.contrast < 0 or settings.color < 0:
            raise ValueError("Finish values must be non-negative")

        result = ImageEnhance.Contrast(image).enhance(settings.contrast)
        return ImageEnhance.Color(result).enhance(settings.color)
