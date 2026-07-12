from __future__ import annotations

from collections.abc import Iterable

from reality_glitch.domain.exceptions import (
    DuplicateEffectError,
    UnknownEffectError,
)
from reality_glitch.domain.models import EffectDefinition, EffectId
from reality_glitch.domain.ports import ImageEffect


class InMemoryEffectRegistry:
    """Read-only registry of image effects keyed by EffectId."""

    def __init__(self, effects: Iterable[ImageEffect]) -> None:
        registered: dict[EffectId, ImageEffect] = {}

        for effect in effects:
            effect_id = effect.definition.effect_id
            if effect_id in registered:
                raise DuplicateEffectError(
                    f"Effect is already registered: {effect_id}"
                )
            registered[effect_id] = effect

        self._effects = registered

    def get(self, effect_id: EffectId) -> ImageEffect:
        try:
            return self._effects[effect_id]
        except KeyError as error:
            raise UnknownEffectError(f"Unknown effect: {effect_id}") from error

    def list_definitions(self) -> tuple[EffectDefinition, ...]:
        return tuple(effect.definition for effect in self._effects.values())
