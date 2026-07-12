from __future__ import annotations

from dataclasses import dataclass

from reality_glitch.domain.models import EffectStep, FinishSettings, Preset


@dataclass(slots=True)
class EditorState:
    steps: list[EffectStep]
    finish: FinishSettings
    active_preset: str

    @classmethod
    def from_preset(cls, preset: Preset) -> EditorState:
        return cls(
            steps=list(preset.steps),
            finish=preset.finish,
            active_preset=preset.name,
        )
