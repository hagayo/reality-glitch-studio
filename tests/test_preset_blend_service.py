from __future__ import annotations

import pytest

from reality_glitch.container import build_container
from reality_glitch.services.preset_blend_service import PresetBlendService


def test_preset_blender_rejects_invalid_ratio() -> None:
    blender = PresetBlendService()
    container = build_container()
    with pytest.raises(ValueError, match="ratio"):
        blender.blend(container.presets.get("Cyber Pulse"), container.presets.get("Mirror Gloss"), 1.5)


def test_preset_blender_returns_named_preset() -> None:
    blender = PresetBlendService()
    container = build_container()
    result = blender.blend(container.presets.get("Cyber Pulse"), container.presets.get("Mirror Gloss"), 0.5)
    assert result.name.startswith("Blend:")
    assert result.steps


def test_preset_blender_interpolates_finish_settings() -> None:
    blender = PresetBlendService()
    container = build_container()
    preset_a = container.presets.get("Mirror Gloss")
    preset_b = container.presets.get("Cinema Noir")
    result = blender.blend(preset_a, preset_b, 0.5)
    expected_contrast = (preset_a.finish.contrast + preset_b.finish.contrast) / 2
    assert result.finish.contrast == expected_contrast
