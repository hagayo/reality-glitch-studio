from __future__ import annotations

import math
import numpy as np

from PIL import Image, ImageEnhance, ImageOps


def prepare_image( image: Image.Image, max_size: int = 1200, ) -> Image.Image:
    """
    Convert an uploaded image to RGB and reduce very large images.
    Limiting the image size keeps processing fast and reduces memory usage.
    """
    prepared = ImageOps.exif_transpose(image).convert("RGB")
    prepared.thumbnail((max_size, max_size))
    return prepared


def wave_effect( image: Image.Image, amplitude: int = 25, frequency: float = 3.0, vertical: bool = False, ) -> Image.Image:
    """
    Move rows or columns according to a sine wave.
    amplitude: Maximum number of pixels moved.
    frequency: Number of wave cycles across the image. 
    vertical: False moves rows horizontally. 
    True moves columns vertically.
    """
    pixels = np.array(image)
    result = np.empty_like(pixels)
    height, width = pixels.shape[:2]
    if vertical:
        for x in range(width):
            angle = 2 * math.pi * frequency * x / max(width, 1)
            shift = int(amplitude * math.sin(angle))
            result[:, x] = np.roll(pixels[:, x], shift, axis=0)
    else:
        for y in range(height):
            angle = 2 * math.pi * frequency * y / max(height, 1)
            shift = int(amplitude * math.sin(angle))
            result[y] = np.roll(pixels[y], shift, axis=0)
    return Image.fromarray(result)


def glitch_effect( image: Image.Image, intensity: int = 40, block_count: int = 20, seed: int = 42, ) -> Image.Image:
    """ 
    Shift random horizontal image blocks.
    A seed is used so the same settings can reproduce the same result. 
    """
    rng = np.random.default_rng(seed)
    pixels = np.array(image) 
    result = pixels.copy() 
    height, width = pixels.shape[:2] 
    if height < 2 or width < 2:
        return image.copy()
    max_block_height = max(2, height // 8)
    for _ in range(block_count):
        block_height = int(rng.integers(2, max_block_height + 1))
        start_y = int(rng.integers(0, max(1, height - block_height + 1)))
        end_y = min(start_y + block_height, height)
        shift = int(rng.integers(-intensity, intensity + 1))
        result[start_y:end_y] = np.roll( result[start_y:end_y], shift, axis=1, )
    return Image.fromarray(result)


def rgb_split_effect( image: Image.Image, distance: int = 15, ) -> Image.Image:
    """
    Separate the red, green and blue channels. 
    This creates a digital chromatic distortion.
    """
    pixels = np.array(image)
    red = pixels[:, :, 0]
    green = pixels[:, :, 1]
    blue = pixels[:, :, 2]
    result = np.zeros_like(pixels)
    result[:, :, 0] = np.roll(red, distance, axis=1) 
    result[:, :, 1] = green 
    result[:, :, 2] = np.roll(blue, -distance, axis=1) 
    return Image.fromarray(result)


def mirror_effect( image: Image.Image, mode: str = "left", ) -> Image.Image:
    """ Create an impossible symmetry by mirroring part of the image. """
    pixels = np.array(image)
    height, width = pixels.shape[:2] 
    result = pixels.copy() 
    middle = width // 2 
    if mode == "left":
        left_half = pixels[:, :middle]
        mirrored = np.flip(left_half, axis=1)
        result[:, width - mirrored.shape[1] :] = mirrored
    elif mode == "right":
        right_half = pixels[:, width - middle :] 
        mirrored = np.flip(right_half, axis=1) 
        result[:, : mirrored.shape[1]] = mirrored 
    elif mode == "top": 
        middle_y = height // 2 
        top_half = pixels[:middle_y] 
        mirrored = np.flip(top_half, axis=0) 
        result[height - mirrored.shape[0] :] = mirrored 
    elif mode == "bottom":
        middle_y = height // 2 
        bottom_half = pixels[height - middle_y :] 
        mirrored = np.flip(bottom_half, axis=0) 
        result[: mirrored.shape[0]] = mirrored 
    else:
        raise ValueError(f"Unsupported mirror mode: {mode}")
    
    return Image.fromarray(result)


def portal_effect( image: Image.Image, repetitions: int = 6, scale: float = 0.72, rotation: int = 4, ) -> Image.Image:
    """
    Place smaller versions of the image inside itself. 
    Each repeated image becomes smaller and can be slightly rotated.
    """
    result = image.copy()
    canvas_width, canvas_height = result.size 
    current_width = canvas_width 
    current_height = canvas_height 
    for index in range(1, repetitions + 1):
        current_width = int(current_width * scale)
        current_height = int(current_height * scale)
        if current_width < 10 or current_height < 10:
            break
        smaller = image.resize( (current_width, current_height), Image.Resampling.LANCZOS, ) 
        current_rotation = rotation * index 
        if current_rotation:
            smaller = smaller.rotate( current_rotation, resample=Image.Resampling.BICUBIC, expand=True, ) 
        x = (canvas_width - smaller.width) // 2 
        y = (canvas_height - smaller.height) // 2 
        result.paste(smaller, (x, y)) 
    return result


def enhance_result( image: Image.Image, contrast: float = 1.0, color: float = 1.0, ) -> Image.Image:
    """ Apply optional finishing adjustments. """ 
    result = ImageEnhance.Contrast(image).enhance(contrast) 
    result = ImageEnhance.Color(result).enhance(color) 
    return result


# FUTURE EFFECTS:
# Pixel Sort
# Kaleidoscope
# Mosaic
# Scan Lines
# Color Inversion
# Circular Ripple
# Broken Television
# Melting Image
# Repeated Strips
# Brightness-Based Shift

# effects pipeline:
# result = first_effect(image) result = second_effect(result) result = third_effect(result)

# add to .github/workflows/ci.yml:
# uv sync
# uv run pytest
# uv run ruff check .
# uv run ruff format --check .

# Add MIT License