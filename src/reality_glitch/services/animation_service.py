from __future__ import annotations

from io import BytesIO
from math import pi, sin

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
        if options.mode == "build_up":
            frames = self._render_build_up_frames(image, request, options)
        elif options.mode == "parameter":
            frames = self._render_parameter_frames(image, request, options)
        else:
            frames = self._render_ping_pong_frames(image, request, options)

        if options.mode == "ping_pong" and options.ping_pong and len(frames) > 2:
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

    def _render_ping_pong_frames(
        self,
        image: Image.Image,
        request: PipelineRequest,
        options: AnimationOptions,
    ) -> list[Image.Image]:
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
            frames.append(frame.convert("P", palette=Image.Palette.ADAPTIVE))
        return frames

    def _render_build_up_frames(
        self,
        image: Image.Image,
        request: PipelineRequest,
        options: AnimationOptions,
    ) -> list[Image.Image]:
        step_count = max(1, len(request.steps))
        frames: list[Image.Image] = []
        for frame_index in range(options.frame_count):
            overall_progress = frame_index / (options.frame_count - 1)
            scaled = overall_progress * step_count
            current_step_index = min(step_count - 1, int(scaled))
            intra_progress = min(1.0, scaled - current_step_index)
            animated_steps: list[EffectStep] = []
            for index, step in enumerate(request.steps):
                if index < current_step_index:
                    animated_steps.append(step)
                elif index == current_step_index:
                    animated_steps.append(self._animate_step(step, intra_progress, frame_index))
                    break
                else:
                    break
            frame_request = PipelineRequest(
                steps=tuple(animated_steps),
                finish=request.finish,
            )
            frame = self._pipeline.execute(image, frame_request).image
            frames.append(frame.convert("P", palette=Image.Palette.ADAPTIVE))
        return frames

    def _render_parameter_frames(
        self,
        image: Image.Image,
        request: PipelineRequest,
        options: AnimationOptions,
    ) -> list[Image.Image]:
        frames: list[Image.Image] = []
        for frame_index in range(options.frame_count):
            progress = frame_index / (options.frame_count - 1)
            oscillation = sin(progress * 2 * pi)
            animated_steps: list[EffectStep] = []
            for index, step in enumerate(request.steps):
                settings = dict(step.settings)
                if index == options.animated_step_index and options.animated_parameter:
                    current = settings.get(options.animated_parameter)
                    if isinstance(current, (int, float)):
                        factor = 1.0 + (options.parameter_swing * oscillation)
                        value = current * factor
                        if isinstance(current, int) and not isinstance(current, bool):
                            value = int(round(value))
                        settings[options.animated_parameter] = value
                animated_steps.append(EffectStep(step.effect_id, settings))
            frame_request = PipelineRequest(
                steps=tuple(animated_steps),
                finish=request.finish,
            )
            frame = self._pipeline.execute(image, frame_request).image
            frames.append(frame.convert("P", palette=Image.Palette.ADAPTIVE))
        return frames

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
