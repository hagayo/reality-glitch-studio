from __future__ import annotations

from io import BytesIO

from PIL import Image

from reality_glitch.domain.models import (
    AnimationOptions,
    EffectStep,
    PipelineRequest,
)
from reality_glitch.domain.ports import EffectRegistry, PipelineProcessor


class GifAnimationService:
    def __init__(
        self,
        registry: EffectRegistry,
        pipeline: PipelineProcessor,
    ) -> None:
        self._registry = registry
        self._pipeline = pipeline

    def render_gif(
        self,
        image: Image.Image,
        request: PipelineRequest,
        options: AnimationOptions,
    ) -> bytes:
        frames: list[Image.Image] = []

        for frame_index in range(options.frame_count):
            progress = frame_index / (options.frame_count - 1)
            animated_steps = tuple(
                self._animate_step(step, progress, frame_index)
                for step in request.steps
            )
            frame_request = PipelineRequest(
                steps=animated_steps,
                finish=request.finish,
            )
            frame = self._pipeline.execute(image, frame_request).image
            frames.append(
                frame.convert("P", palette=Image.Palette.ADAPTIVE)
            )

        if options.ping_pong and len(frames) > 2:
            frames += frames[-2:0:-1]

        buffer = BytesIO()
        frames[0].save(
            buffer,
            format="GIF",
            save_all=True,
            append_images=frames[1:],
            duration=options.frame_duration_ms,
            loop=0,
            optimize=True,
        )
        return buffer.getvalue()

    def _animate_step(
        self,
        step: EffectStep,
        progress: float,
        frame_index: int,
    ) -> EffectStep:
        effect = self._registry.get(step.effect_id)
        settings = effect.settings_for_frame(
            dict(step.settings),
            progress,
            frame_index,
        )
        return EffectStep(step.effect_id, settings)
