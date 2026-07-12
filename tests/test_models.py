from __future__ import annotations

import pytest

from reality_glitch.domain.models import (
    AnimationOptions,
    EffectId,
    EffectStep,
    FinishSettings,
    PipelineRequest,
)


def test_effect_step_with_settings_returns_new_instance() -> None:
    original = EffectStep(EffectId.WAVE, {"amplitude": 10})

    changed = original.with_settings(amplitude=20, frequency=2.0)

    assert original.settings == {"amplitude": 10}
    assert changed.settings == {"amplitude": 20, "frequency": 2.0}
    assert changed is not original


def test_pipeline_request_defaults_are_stable() -> None:
    first = PipelineRequest(steps=())
    second = PipelineRequest(steps=())

    assert first.finish == FinishSettings()
    assert second.finish == FinishSettings()


@pytest.mark.parametrize("frame_count", [0, 1, -1])
def test_animation_options_reject_too_few_frames(frame_count: int) -> None:
    with pytest.raises(ValueError, match="frame_count"):
        AnimationOptions(frame_count=frame_count)


@pytest.mark.parametrize("duration", [0, 1, 19, -10])
def test_animation_options_reject_too_short_duration(duration: int) -> None:
    with pytest.raises(ValueError, match="frame_duration_ms"):
        AnimationOptions(frame_duration_ms=duration)


def test_animation_options_accept_boundary_values() -> None:
    options = AnimationOptions(frame_count=2, frame_duration_ms=20)

    assert options.frame_count == 2
    assert options.frame_duration_ms == 20


def test_animation_options_reject_unknown_mode() -> None:
    with pytest.raises(ValueError, match="mode"):
        AnimationOptions(mode="weird")
