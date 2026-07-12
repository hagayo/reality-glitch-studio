class RealityGlitchError(Exception):
    """Base exception for expected application failures."""


class UnknownEffectError(RealityGlitchError):
    """Raised when an effect identifier is not registered."""


class DuplicateEffectError(RealityGlitchError):
    """Raised when two effects use the same identifier."""


class InvalidEffectOutputError(RealityGlitchError):
    """Raised when an effect does not return a valid Pillow image."""


class UnknownPresetError(RealityGlitchError):
    """Raised when a requested preset does not exist."""


class InvalidImageError(RealityGlitchError):
    """Raised when an image cannot be prepared or processed."""
