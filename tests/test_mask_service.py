from __future__ import annotations

from PIL import Image

from reality_glitch.services.mask_service import (
    build_mask_image,
    build_mask_overlay,
    combine_mask_images,
    resolve_mask_cells,
)


def test_resolve_mask_cells_for_background_excludes_center() -> None:
    cells = resolve_mask_cells({"preset": "background"})
    assert "1-1" not in cells
    assert len(cells) == 8


def test_build_mask_image_returns_none_when_no_cells_selected() -> None:
    assert build_mask_image((90, 90), {"preset": "custom", "selected_cells": []}) is None


def test_build_mask_image_creates_mask() -> None:
    mask = build_mask_image((90, 90), {"preset": "center", "feather": 0})
    assert mask is not None
    assert mask.getbbox() is not None


def test_combine_mask_images_merges_multiple_regions() -> None:
    combined = combine_mask_images(
        (90, 90),
        [
            {"preset": "left", "feather": 0},
            {"preset": "right", "feather": 0},
        ],
    )
    assert combined is not None
    assert combined.getbbox() == (0, 0, 90, 90)


def test_build_mask_overlay_changes_selected_region() -> None:
    image = Image.new("RGB", (90, 90), "black")
    overlay = build_mask_overlay(
        image,
        [{"preset": "center", "feather": 0}],
        opacity=128,
        show_grid=False,
    )
    assert overlay.getpixel((45, 45)) != (0, 0, 0)
    assert overlay.getpixel((5, 5)) == (0, 0, 0)


def test_build_mask_overlay_rejects_invalid_opacity() -> None:
    image = Image.new("RGB", (20, 20), "black")
    import pytest
    with pytest.raises(ValueError, match="opacity"):
        build_mask_overlay(image, [{"preset": "center"}], opacity=300)
