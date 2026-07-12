from __future__ import annotations

import numpy as np
import pytest
from PIL import Image, ImageChops

from reality_glitch.effects import (
    GlitchEffect,
    GrayscaleEffect,
    MirrorEffect,
    PortalEffect,
    RgbSplitEffect,
    WaveEffect,
)


EFFECT_CASES = [
    (WaveEffect(), {"amplitude": 10, "frequency": 2.0}),
    (GlitchEffect(), {"intensity": 10, "block_count": 3, "seed": 1}),
    (GrayscaleEffect(), {}),
    (RgbSplitEffect(), {"distance": 3}),
    (MirrorEffect(), {"mode": "left"}),
    (PortalEffect(), {"repetitions": 2, "scale": 0.7, "rotation": 2}),
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
