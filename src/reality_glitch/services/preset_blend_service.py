from __future__ import annotations

from typing import Any

from reality_glitch.domain.models import EffectId, EffectStep, FinishSettings, Preset


class PresetBlendService:
    def blend(self, preset_a: Preset, preset_b: Preset, ratio: float) -> Preset:
        if not 0.0 <= ratio <= 1.0:
            raise ValueError("ratio must be between 0 and 1")

        steps = self._blend_steps(preset_a.steps, preset_b.steps, ratio)
        finish = FinishSettings(
            contrast=self._interpolate_number(preset_a.finish.contrast, preset_b.finish.contrast, ratio),
            color=self._interpolate_number(preset_a.finish.color, preset_b.finish.color, ratio),
        )
        name = f"Blend: {preset_a.name} ↔ {preset_b.name} ({round(ratio * 100)}%)"
        return Preset(name=name, steps=steps, finish=finish)

    def _blend_steps(
        self,
        steps_a: tuple[EffectStep, ...],
        steps_b: tuple[EffectStep, ...],
        ratio: float,
    ) -> tuple[EffectStep, ...]:
        step_map_a = {step.effect_id: step for step in steps_a}
        step_map_b = {step.effect_id: step for step in steps_b}

        ordered_effects: list[EffectId] = []
        for step in steps_a:
            if step.effect_id not in ordered_effects:
                ordered_effects.append(step.effect_id)
        for step in steps_b:
            if step.effect_id not in ordered_effects:
                ordered_effects.append(step.effect_id)

        blended_steps: list[EffectStep] = []
        for effect_id in ordered_effects:
            step_a = step_map_a.get(effect_id)
            step_b = step_map_b.get(effect_id)
            if step_a and step_b:
                blended_steps.append(self._blend_step(step_a, step_b, ratio))
            elif step_a and ratio < 0.5:
                blended_steps.append(step_a)
            elif step_b and ratio >= 0.5:
                blended_steps.append(step_b)

        return tuple(blended_steps[:6])

    def _blend_step(self, step_a: EffectStep, step_b: EffectStep, ratio: float) -> EffectStep:
        keys = set(step_a.settings) | set(step_b.settings)
        blended_settings: dict[str, Any] = {}
        for key in keys:
            value_a = step_a.settings.get(key)
            value_b = step_b.settings.get(key)
            blended_settings[key] = self._blend_value(value_a, value_b, ratio)

        blended_mask = self._blend_mask(step_a.mask, step_b.mask, ratio)
        return EffectStep(step_a.effect_id, blended_settings, blended_mask)

    def _blend_mask(self, mask_a: dict[str, Any] | None, mask_b: dict[str, Any] | None, ratio: float) -> dict[str, Any] | None:
        if mask_a and mask_b:
            if ratio < 0.5:
                return dict(mask_a)
            return dict(mask_b)
        if mask_a and ratio < 0.5:
            return dict(mask_a)
        if mask_b and ratio >= 0.5:
            return dict(mask_b)
        return None

    def _blend_value(self, value_a: Any, value_b: Any, ratio: float) -> Any:
        if value_a is None:
            return value_b
        if value_b is None:
            return value_a
        if isinstance(value_a, bool) or isinstance(value_b, bool):
            return value_a if ratio < 0.5 else value_b
        if isinstance(value_a, (int, float)) and isinstance(value_b, (int, float)):
            interpolated = self._interpolate_number(float(value_a), float(value_b), ratio)
            if isinstance(value_a, int) and isinstance(value_b, int):
                return int(round(interpolated))
            return interpolated
        return value_a if ratio < 0.5 else value_b

    @staticmethod
    def _interpolate_number(value_a: float, value_b: float, ratio: float) -> float:
        return value_a + ((value_b - value_a) * ratio)
