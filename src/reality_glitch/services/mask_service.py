from __future__ import annotations

from typing import Any

from PIL import Image, ImageChops, ImageDraw, ImageFilter


MASK_GRID_SIZE = 3


def build_mask_image(size: tuple[int, int], mask_settings: dict[str, Any] | None) -> Image.Image | None:
    if not mask_settings:
        return None

    preset = str(mask_settings.get("preset", "custom"))
    feather = max(0, int(mask_settings.get("feather", 0)))
    selected_cells = resolve_mask_cells(mask_settings)

    if not selected_cells:
        return None

    width, height = size
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    cell_width = width / MASK_GRID_SIZE
    cell_height = height / MASK_GRID_SIZE

    for cell in selected_cells:
        row_index, col_index = parse_cell(cell)
        left = int(round(col_index * cell_width))
        top = int(round(row_index * cell_height))
        right = int(round((col_index + 1) * cell_width))
        bottom = int(round((row_index + 1) * cell_height))
        draw.rectangle((left, top, right, bottom), fill=255)

    if feather > 0:
        mask = mask.filter(ImageFilter.GaussianBlur(radius=feather))
    return mask


def resolve_mask_cells(mask_settings: dict[str, Any]) -> list[str]:
    preset = str(mask_settings.get("preset", "custom"))
    if preset == "custom":
        selected = list(mask_settings.get("selected_cells", []))
        return selected
    if preset == "center":
        return ["1-1"]
    if preset == "background":
        return [cell for cell in all_cells() if cell != "1-1"]
    if preset == "top":
        return [f"0-{column}" for column in range(MASK_GRID_SIZE)]
    if preset == "bottom":
        return [f"2-{column}" for column in range(MASK_GRID_SIZE)]
    if preset == "left":
        return [f"{row}-0" for row in range(MASK_GRID_SIZE)]
    if preset == "right":
        return [f"{row}-2" for row in range(MASK_GRID_SIZE)]
    return []


def all_cells() -> list[str]:
    return [f"{row}-{column}" for row in range(MASK_GRID_SIZE) for column in range(MASK_GRID_SIZE)]


def parse_cell(cell: str) -> tuple[int, int]:
    row_text, column_text = cell.split("-")
    return int(row_text), int(column_text)


def combine_mask_images(size: tuple[int, int], mask_settings_list: list[dict[str, Any]]) -> Image.Image | None:
    combined: Image.Image | None = None
    for mask_settings in mask_settings_list:
        current = build_mask_image(size, mask_settings)
        if current is None:
            continue
        combined = current if combined is None else ImageChops.lighter(combined, current)
    return combined


def build_mask_overlay(
    image: Image.Image,
    mask_settings_list: list[dict[str, Any]],
    opacity: int = 115,
    show_grid: bool = True,
) -> Image.Image:
    if not 0 <= opacity <= 255:
        raise ValueError("opacity must be between 0 and 255")

    base = image.convert("RGBA")
    combined_mask = combine_mask_images(base.size, mask_settings_list)
    if combined_mask is None:
        return base.convert("RGB")

    alpha = combined_mask.point(lambda value: round((value / 255.0) * opacity))
    color_layer = Image.new("RGBA", base.size, (0, 215, 255, 0))
    color_layer.putalpha(alpha)
    preview = Image.alpha_composite(base, color_layer)

    if show_grid:
        draw = ImageDraw.Draw(preview)
        width, height = preview.size
        grid_color = (255, 255, 255, 175)
        for index in range(1, MASK_GRID_SIZE):
            x = round((width / MASK_GRID_SIZE) * index)
            y = round((height / MASK_GRID_SIZE) * index)
            draw.line((x, 0, x, height), fill=grid_color, width=2)
            draw.line((0, y, width, y), fill=grid_color, width=2)

    return preview.convert("RGB")
