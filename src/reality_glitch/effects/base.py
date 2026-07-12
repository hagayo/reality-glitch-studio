from __future__ import annotations

from copy import deepcopy
from typing import Any


class BaseEffect:
    """Shared default animation behavior for stateless effects."""

    def settings_for_frame(
        self,
        settings: dict[str, Any],
        progress: float,
        frame_index: int,
    ) -> dict[str, Any]:
        del progress, frame_index
        return deepcopy(settings)
