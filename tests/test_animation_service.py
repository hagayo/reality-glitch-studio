from __future__ import annotations

from io import BytesIO

from PIL import Image

from reality_glitch.container import build_container
from reality_glitch.domain.models import (
    AnimationOptions,
    EffectId,
    EffectStep,
    PipelineRequest,
)



def patterned_image() -> Image.Image:
    image = Image.new("RGB", (16, 16), "black")
    for x in range(image.width):
        for y in range(image.height):
            image.putpixel((x, y), ((x * 17) % 256, (y * 23) % 256, (x * y) % 256))
    return image

def open_gif(data: bytes) -> Image.Image:
    image = Image.open(BytesIO(data))
    image.load()
    return image


def test_animation_returns_openable_gif() -> None:
    container = build_container()
    image = Image.new("RGB", (24, 24), "orange")
    request = PipelineRequest(
        steps=(EffectStep(EffectId.RGB_SPLIT, {"distance": 4}),)
    )

    data = container.animation.render_gif(
        image,
        request,
        AnimationOptions(frame_count=3, frame_duration_ms=50),
    )

    assert data.startswith(b"GIF")
    reopened = open_gif(data)
    assert reopened.format == "GIF"
    assert reopened.size == image.size


def test_animation_without_ping_pong_has_requested_frame_count() -> None:
    container = build_container()
    data = container.animation.render_gif(
        patterned_image(),
        PipelineRequest(
            steps=(EffectStep(EffectId.WAVE, {"amplitude": 5}),)
        ),
        AnimationOptions(
            frame_count=4,
            frame_duration_ms=50,
            ping_pong=False,
        ),
    )

    reopened = open_gif(data)

    assert reopened.n_frames == 4


def test_ping_pong_adds_reverse_frames_without_duplicate_edges() -> None:
    container = build_container()
    data = container.animation.render_gif(
        patterned_image(),
        PipelineRequest(
            steps=(EffectStep(EffectId.WAVE, {"amplitude": 8}),)
        ),
        AnimationOptions(frame_count=5, frame_duration_ms=50, ping_pong=True),
    )

    reopened = open_gif(data)

    assert reopened.n_frames == 8


def test_animation_does_not_mutate_request_settings() -> None:
    container = build_container()
    settings = {"distance": 5}
    request = PipelineRequest(
        steps=(EffectStep(EffectId.RGB_SPLIT, settings),)
    )

    container.animation.render_gif(
        Image.new("RGB", (8, 8), "orange"),
        request,
        AnimationOptions(frame_count=2, frame_duration_ms=20),
    )

    assert settings == {"distance": 5}
