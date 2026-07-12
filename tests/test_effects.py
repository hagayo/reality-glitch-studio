from __future__ import annotations

import numpy as np
import pytest
from PIL import Image, ImageChops

from reality_glitch.effects import (
    CircularRippleEffect,
    GlitchEffect,
    GrayscaleEffect,
    KaleidoscopeEffect,
    MirrorEffect,
    MosaicEffect,
    PixelSortEffect,
    PortalEffect,
    RetroCrtEffect,
    RgbSplitEffect,
    SwirlEffect,
    WaveEffect,
)


EFFECT_CASES = [
    (WaveEffect(), {"amplitude": 10, "frequency": 2.0}),
    (GlitchEffect(), {"intensity": 10, "block_count": 3, "seed": 1}),
    (GrayscaleEffect(), {}),
    (RgbSplitEffect(), {"distance": 3}),
    (MirrorEffect(), {"mode": "left"}),
    (PortalEffect(), {"repetitions": 2, "scale": 0.7, "rotation": 2}),
    (PixelSortEffect(), {"orientation": "horizontal", "threshold": 100, "min_segment_length": 4}),
    (KaleidoscopeEffect(), {"segments": 5, "rotation_degrees": 10.0, "zoom": 1.0}),
    (CircularRippleEffect(), {"amplitude": 8, "wavelength": 18, "phase_degrees": 0.0}),
    (MosaicEffect(), {"block_size": 6}),
    (SwirlEffect(), {"strength": 2.0, "radius": 40.0}),
    (RetroCrtEffect(), {"scanline_strength": 0.2, "line_spacing": 3, "channel_shift": 1, "noise_strength": 0.01, "seed": 3}),
]


@pytest.mark.parametrize("effect, settings", EFFECT_CASES)
def test_effect_preserves_image_size_and_mode(
    effect,
    settings,
    rgb_image: Image.Image,
) -> None:
    result = effect.apply(rgb_image, settings)

    assert result.size == rgb_image.size
    assert result.mode == "RGB"


@pytest.mark.parametrize("effect, settings", EFFECT_CASES)
def test_effect_does_not_mutate_source(
    effect,
    settings,
    rgb_image: Image.Image,
) -> None:
    before = rgb_image.copy()

    effect.apply(rgb_image, settings)

    assert ImageChops.difference(rgb_image, before).getbbox() is None


@pytest.mark.parametrize("effect, settings", EFFECT_CASES)
def test_effect_handles_one_pixel_image(
    effect,
    settings,
    tiny_image: Image.Image,
) -> None:
    result = effect.apply(tiny_image, settings)

    assert result.size == (1, 1)


def test_wave_zero_amplitude_is_identity(rgb_image: Image.Image) -> None:
    result = WaveEffect().apply(rgb_image, {"amplitude": 0, "frequency": 4})

    assert ImageChops.difference(result, rgb_image).getbbox() is None


def test_wave_supports_vertical_mode(rgb_image: Image.Image) -> None:
    result = WaveEffect().apply(
        rgb_image,
        {"amplitude": 5, "frequency": 2, "vertical": True},
    )

    assert result.size == rgb_image.size


def test_glitch_same_seed_is_deterministic(rgb_image: Image.Image) -> None:
    settings = {"intensity": 20, "block_count": 6, "seed": 100}

    first = GlitchEffect().apply(rgb_image, settings)
    second = GlitchEffect().apply(rgb_image, settings)

    assert ImageChops.difference(first, second).getbbox() is None


def test_glitch_normalizes_zero_values(rgb_image: Image.Image) -> None:
    result = GlitchEffect().apply(
        rgb_image,
        {"intensity": 0, "block_count": 0, "seed": 1},
    )

    assert result.size == rgb_image.size


def test_rgb_split_zero_distance_is_identity(rgb_image: Image.Image) -> None:
    result = RgbSplitEffect().apply(rgb_image, {"distance": 0})

    assert ImageChops.difference(result, rgb_image).getbbox() is None


@pytest.mark.parametrize("mode", ["left", "right", "top", "bottom"])
def test_mirror_supports_all_modes(mode: str, rgb_image: Image.Image) -> None:
    result = MirrorEffect().apply(rgb_image, {"mode": mode})

    assert result.size == rgb_image.size


def test_mirror_rejects_unknown_mode(rgb_image: Image.Image) -> None:
    with pytest.raises(ValueError):
        MirrorEffect().apply(rgb_image, {"mode": "diagonal"})


@pytest.mark.parametrize("scale", [0, -0.1, 1.0, 1.1])
def test_portal_rejects_invalid_scale(scale: float, rgb_image: Image.Image) -> None:
    with pytest.raises(ValueError, match="scale"):
        PortalEffect().apply(rgb_image, {"scale": scale})


def test_portal_rejects_negative_repetitions(rgb_image: Image.Image) -> None:
    with pytest.raises(ValueError, match="repetitions"):
        PortalEffect().apply(rgb_image, {"repetitions": -1})


def test_portal_zero_repetitions_is_identity(rgb_image: Image.Image) -> None:
    result = PortalEffect().apply(
        rgb_image,
        {"repetitions": 0, "scale": 0.7, "rotation": 5},
    )

    assert ImageChops.difference(result, rgb_image).getbbox() is None


def test_pixel_sort_high_threshold_is_identity(rgb_image: Image.Image) -> None:
    result = PixelSortEffect().apply(
        rgb_image,
        {"orientation": "horizontal", "threshold": 255, "reverse": False},
    )

    assert ImageChops.difference(result, rgb_image).getbbox() is None


def test_pixel_sort_supports_vertical_sort(rgb_image: Image.Image) -> None:
    result = PixelSortEffect().apply(
        rgb_image,
        {"orientation": "vertical", "threshold": 20, "reverse": True},
    )

    assert result.size == rgb_image.size


def test_pixel_sort_rejects_invalid_orientation(rgb_image: Image.Image) -> None:
    with pytest.raises(ValueError, match="orientation"):
        PixelSortEffect().apply(rgb_image, {"orientation": "diagonal"})


@pytest.mark.parametrize("segments", [0, 1])
def test_kaleidoscope_rejects_too_few_segments(
    segments: int, rgb_image: Image.Image
) -> None:
    with pytest.raises(ValueError, match="segments"):
        KaleidoscopeEffect().apply(rgb_image, {"segments": segments})


@pytest.mark.parametrize("zoom", [0, -0.5])
def test_kaleidoscope_rejects_invalid_zoom(zoom: float, rgb_image: Image.Image) -> None:
    with pytest.raises(ValueError, match="zoom"):
        KaleidoscopeEffect().apply(rgb_image, {"segments": 6, "zoom": zoom})


def test_circular_ripple_zero_amplitude_is_identity(rgb_image: Image.Image) -> None:
    result = CircularRippleEffect().apply(
        rgb_image,
        {"amplitude": 0, "wavelength": 50, "phase_degrees": 0},
    )

    assert ImageChops.difference(result, rgb_image).getbbox() is None


@pytest.mark.parametrize("wavelength", [0, -10])
def test_circular_ripple_rejects_invalid_wavelength(
    wavelength: int, rgb_image: Image.Image
) -> None:
    with pytest.raises(ValueError, match="wavelength"):
        CircularRippleEffect().apply(
            rgb_image,
            {"amplitude": 5, "wavelength": wavelength, "phase_degrees": 0},
        )


@pytest.mark.parametrize("effect, settings", EFFECT_CASES)
def test_animation_settings_do_not_mutate_source(effect, settings) -> None:
    before = dict(settings)

    result = effect.settings_for_frame(settings, 0.5, 2)

    assert settings == before
    assert result is not settings


def test_grayscale_removes_color_channels(rgb_image: Image.Image) -> None:
    result = GrayscaleEffect().apply(rgb_image, {})

    pixels = np.asarray(result)

    assert np.array_equal(pixels[:, :, 0], pixels[:, :, 1])
    assert np.array_equal(pixels[:, :, 1], pixels[:, :, 2])


def test_grayscale_returns_rgb_for_grayscale_input() -> None:
    source = Image.new("L", (4, 3), 120)

    result = GrayscaleEffect().apply(source, {})

    assert result.mode == "RGB"
    assert result.size == source.size


def test_mosaic_rejects_invalid_block_size(rgb_image: Image.Image) -> None:
    with pytest.raises(ValueError, match="block_size"):
        MosaicEffect().apply(rgb_image, {"block_size": 0})


def test_swirl_zero_strength_is_identity(rgb_image: Image.Image) -> None:
    result = SwirlEffect().apply(rgb_image, {"strength": 0.0, "radius": 50.0})

    assert ImageChops.difference(result, rgb_image).getbbox() is None


@pytest.mark.parametrize("radius", [0, -10])
def test_swirl_rejects_invalid_radius(radius: float, rgb_image: Image.Image) -> None:
    with pytest.raises(ValueError, match="radius"):
        SwirlEffect().apply(rgb_image, {"strength": 2.0, "radius": radius})


@pytest.mark.parametrize("line_spacing", [0, -1])
def test_retro_crt_rejects_invalid_line_spacing(line_spacing: int, rgb_image: Image.Image) -> None:
    with pytest.raises(ValueError, match="line_spacing"):
        RetroCrtEffect().apply(rgb_image, {"line_spacing": line_spacing})
