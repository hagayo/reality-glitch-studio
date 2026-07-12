from __future__ import annotations

import pytest
from PIL import Image

from reality_glitch.domain.exceptions import DuplicateEffectError, UnknownEffectError
from reality_glitch.domain.models import EffectDefinition, EffectId
from reality_glitch.infrastructure.registry import InMemoryEffectRegistry


class StubEffect:
    def __init__(self, effect_id: EffectId) -> None:
        self.definition = EffectDefinition(effect_id, effect_id.value)

    def apply(self, image: Image.Image, settings: dict) -> Image.Image:
        return image.copy()

    def settings_for_frame(
        self,
        settings: dict,
        progress: float,
        frame_index: int,
    ) -> dict:
        return dict(settings)


def test_empty_registry_lists_no_definitions() -> None:
    registry = InMemoryEffectRegistry(())

    assert registry.list_definitions() == ()


def test_registry_returns_registered_effect() -> None:
    effect = StubEffect(EffectId.WAVE)
    registry = InMemoryEffectRegistry((effect,))

    assert registry.get(EffectId.WAVE) is effect


def test_registry_reports_unknown_effect() -> None:
    registry = InMemoryEffectRegistry(())

    with pytest.raises(UnknownEffectError, match="Unknown effect"):
        registry.get(EffectId.WAVE)


def test_registry_rejects_duplicate_effect_ids() -> None:
    first = StubEffect(EffectId.WAVE)
    second = StubEffect(EffectId.WAVE)

    with pytest.raises(DuplicateEffectError, match="already registered"):
        InMemoryEffectRegistry((first, second))


def test_registry_preserves_registration_order() -> None:
    registry = InMemoryEffectRegistry(
        (
            StubEffect(EffectId.GLITCH),
            StubEffect(EffectId.WAVE),
        )
    )

    assert [item.effect_id for item in registry.list_definitions()] == [
        EffectId.GLITCH,
        EffectId.WAVE,
    ]
