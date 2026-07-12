from __future__ import annotations

import pytest

from reality_glitch.container import build_container
from reality_glitch.domain.exceptions import UnknownPresetError
from reality_glitch.infrastructure.presets import InMemoryPresetRepository


def test_repository_returns_known_presets() -> None:
    repository = InMemoryPresetRepository()

    assert repository.get("Cyber Pulse").name == "Cyber Pulse"
    assert len(repository.list_all()) >= 32


def test_repository_reports_unknown_preset() -> None:
    repository = InMemoryPresetRepository()

    with pytest.raises(UnknownPresetError):
        repository.get("missing")


def test_preset_names_are_unique() -> None:
    presets = InMemoryPresetRepository().list_all()

    assert len({preset.name for preset in presets}) == len(presets)


def test_every_preset_has_at_least_one_step() -> None:
    for preset in InMemoryPresetRepository().list_all():
        assert preset.steps


def test_every_preset_references_registered_effects() -> None:
    container = build_container()
    registered = {
        definition.effect_id
        for definition in container.registry.list_definitions()
    }

    for preset in container.presets.list_all():
        assert all(step.effect_id in registered for step in preset.steps)


def test_preset_settings_are_not_shared_between_steps() -> None:
    preset = InMemoryPresetRepository().get("Cyber Pulse")

    assert preset.steps[0].settings is not preset.steps[1].settings


@pytest.mark.parametrize(
    "preset_name",
    [
        "Mirror Gloss",
        "Dramatic Black & White",
        "Cinema Noir",
        "Chrome Tunnel",
        "Neon Fracture",
        "Electric Wave",
        "Infinite Reflection",
        "Sorted Spectrum",
        "Crystal Bloom",
        "Ripple Dream",
        "Prism Storm",
        "Aurora Bloom",
        "Melted Skyline",
        "Noir Spiral",
        "Glass Echo",
        "Static Tide",
        "Mosaic Pop",
        "Twisted Center",
        "Retro Broadcast",
        "Retro Mosaic",
        "Vortex Bloom",
        "Focus Pop",
        "Bubble Portrait",
        "Implosion",
        "Twirl Focus",
        "Ghost Merge",
        "Palette Dream",
    ],
)
def test_style_presets_exist(preset_name: str) -> None:
    repository = InMemoryPresetRepository()

    assert repository.get(preset_name).name == preset_name


def test_black_and_white_presets_start_with_grayscale() -> None:
    repository = InMemoryPresetRepository()

    for name in ("Dramatic Black & White", "Cinema Noir"):
        preset = repository.get(name)
        assert preset.steps[0].effect_id.value == "grayscale"
