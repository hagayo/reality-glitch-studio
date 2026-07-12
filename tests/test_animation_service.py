from __future__ import annotations

from PIL import Image

from reality_glitch.container import build_container
from reality_glitch.domain.models import AnimationOptions, EffectId, EffectStep, FinishSettings, PipelineRequest


def test_animation_service_renders_ping_pong_gif() -> None:
    container = build_container()
    image = Image.new("RGB", (32, 32), "red")
    request = PipelineRequest(
        steps=(EffectStep(EffectId.WAVE, {"amplitude": 8, "frequency": 2.0}),),
        finish=FinishSettings(),
    )
    gif_data = container.animation.render_gif(
        image,
        request,
        AnimationOptions(frame_count=6, frame_duration_ms=80, mode="ping_pong"),
    )
    assert gif_data[:6] in {b"GIF87a", b"GIF89a"}


def test_animation_service_renders_build_up_gif() -> None:
    container = build_container()
    image = Image.new("RGB", (32, 32), "red")
    request = PipelineRequest(
        steps=(
            EffectStep(EffectId.WAVE, {"amplitude": 8, "frequency": 2.0}),
            EffectStep(EffectId.RGB_SPLIT, {"distance": 4}),
        ),
        finish=FinishSettings(),
    )
    gif_data = container.animation.render_gif(
        image,
        request,
        AnimationOptions(frame_count=8, frame_duration_ms=80, mode="build_up"),
    )
    assert gif_data[:6] in {b"GIF87a", b"GIF89a"}


def test_animation_service_renders_parameter_gif() -> None:
    container = build_container()
    image = Image.new("RGB", (32, 32), "red")
    request = PipelineRequest(
        steps=(EffectStep(EffectId.CIRCULAR_RIPPLE, {"amplitude": 8, "wavelength": 18, "phase_degrees": 0.0}),),
        finish=FinishSettings(),
    )
    gif_data = container.animation.render_gif(
        image,
        request,
        AnimationOptions(
            frame_count=8,
            frame_duration_ms=80,
            mode="parameter",
            animated_step_index=0,
            animated_parameter="amplitude",
            parameter_swing=0.5,
        ),
    )
    assert gif_data[:6] in {b"GIF87a", b"GIF89a"}
