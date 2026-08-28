#!/usr/bin/env python3
"""Compose approved pet-head images into a dense stack or orderly grid."""

from __future__ import annotations

import argparse
import math
from pathlib import Path
import random
import warnings

from PIL import Image, ImageDraw, ImageFilter, ImageOps


MAX_CANVAS_PIXELS = 40_000_000
MAX_INPUTS = 100
Image.MAX_IMAGE_PIXELS = 50_000_000


def parse_color(value: str) -> tuple[int, int, int, int]:
    value = value.strip().lstrip("#")
    if len(value) == 6:
        value += "ff"
    if len(value) != 8:
        raise argparse.ArgumentTypeError("color must be RRGGBB or RRGGBBAA")
    try:
        return tuple(int(value[i : i + 2], 16) for i in range(0, 8, 2))  # type: ignore[return-value]
    except ValueError as exc:
        raise argparse.ArgumentTypeError("color must be hexadecimal") from exc


def load_image(path: Path) -> Image.Image:
    with warnings.catch_warnings():
        warnings.simplefilter("error", Image.DecompressionBombWarning)
        with Image.open(path) as source:
            source.load()
            return source.convert("RGBA")


def remove_edge_white(image: Image.Image, threshold: int = 245) -> Image.Image:
    if image.getchannel("A").getextrema()[0] < 255:
        return image

    regions = image.convert("L").point(lambda value: 0 if value >= threshold else 255)
    for seed in ((0, 0), (regions.width - 1, 0), (0, regions.height - 1), (regions.width - 1, regions.height - 1)):
        if regions.getpixel(seed) == 0:
            ImageDraw.floodfill(regions, seed, 128, thresh=0)
    image.putalpha(regions.point(lambda value: 0 if value == 128 else 255))
    return image


def prepare_cutout(path: Path, remove_background: bool, require_alpha: bool) -> Image.Image:
    image = load_image(path)
    if require_alpha and image.getchannel("A").getextrema()[0] == 255:
        raise ValueError(f"input is opaque; create a transparent subject cutout first: {path}")
    if remove_background:
        image = remove_edge_white(image)
    bounds = image.getbbox()
    if bounds is None:
        raise ValueError(f"input contains no visible pixels: {path}")
    return image.crop(bounds)


def fit_long_edge(image: Image.Image, target: int) -> Image.Image:
    scale = target / max(image.size)
    size = (max(1, round(image.width * scale)), max(1, round(image.height * scale)))
    return image.resize(size, Image.Resampling.LANCZOS)


def add_outline(image: Image.Image, width: int) -> Image.Image:
    if width <= 0:
        return image
    padded = ImageOps.expand(image, border=width * 2, fill=(0, 0, 0, 0))
    kernel = width * 2 + 1
    outline_alpha = padded.getchannel("A").filter(ImageFilter.MaxFilter(kernel))
    outline = Image.new("RGBA", padded.size, (255, 255, 255, 0))
    outline.putalpha(outline_alpha)
    return Image.alpha_composite(outline, padded)


def add_shadow(image: Image.Image, blur: int, offset_y: int, opacity: int) -> Image.Image:
    if blur <= 0 or opacity <= 0:
        return image
    padding = blur * 3 + abs(offset_y)
    size = (image.width + padding * 2, image.height + padding * 2)
    shadow_alpha = Image.new("L", size, 0)
    shadow_alpha.paste(image.getchannel("A"), (padding, padding + offset_y))
    shadow_alpha = shadow_alpha.filter(ImageFilter.GaussianBlur(blur))
    shadow_alpha = shadow_alpha.point(lambda value: round(value * opacity / 255))
    shadow = Image.new("RGBA", size, (72, 72, 72, 0))
    shadow.putalpha(shadow_alpha)
    foreground = Image.new("RGBA", size, (0, 0, 0, 0))
    foreground.alpha_composite(image, (padding, padding))
    return Image.alpha_composite(shadow, foreground)


def finish_tile(image: Image.Image, args: argparse.Namespace, angle: float = 0) -> Image.Image:
    tile = add_outline(image, args.outline)
    if angle:
        tile = tile.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)
    return add_shadow(tile, args.shadow_blur, args.shadow_offset_y, args.shadow_opacity)


def compose_stack(canvas: Image.Image, sources: list[Image.Image], args: argparse.Namespace) -> None:
    rng = random.Random(args.seed)
    base = max(64, round(args.width * args.tile_scale))
    canvas_area = args.width * args.height
    initial_count = max(len(sources), math.ceil(canvas_area / (base * base) * 2.2))
    max_count = initial_count + math.ceil(canvas_area / (base * base) * 3.0)
    coverage = Image.new("L", canvas.size, 0)
    deck = list(range(len(sources)))
    rng.shuffle(deck)

    def place(index: int, center_x: float, center_y: float) -> None:
        if index and index % len(deck) == 0:
            rng.shuffle(deck)
        source = sources[deck[index % len(deck)]]
        scale = rng.uniform(0.72, 1.28)
        tile = fit_long_edge(source, round(base * scale))
        angle = rng.uniform(-args.rotation, args.rotation)
        tile = finish_tile(tile, args, angle)
        x = round(center_x - tile.width / 2)
        y = round(center_y - tile.height / 2)
        canvas.alpha_composite(tile, (x, y))
        coverage.paste(255, (x, y), tile.getchannel("A"))

    edge = base * 0.18
    for index in range(initial_count):
        place(index, rng.uniform(-edge, args.width + edge), rng.uniform(-edge, args.height + edge))

    sample_step = max(28, base // 7)
    index = initial_count
    while index < max_count:
        uncovered = [
            (x, y)
            for y in range(sample_step // 2, args.height, sample_step)
            for x in range(sample_step // 2, args.width, sample_step)
            if coverage.getpixel((x, y)) < 96
        ]
        if len(uncovered) <= max(1, round(args.width * args.height / (sample_step * sample_step) * 0.025)):
            break
        center_x, center_y = rng.choice(uncovered)
        jitter = sample_step * 0.6
        place(index, center_x + rng.uniform(-jitter, jitter), center_y + rng.uniform(-jitter, jitter))
        index += 1


def compose_grid(canvas: Image.Image, sources: list[Image.Image], args: argparse.Namespace) -> None:
    rows = (len(sources) + args.columns - 1) // args.columns
    usable_width = args.width - 2 * args.padding - (args.columns - 1) * args.gap
    usable_height = args.height - 2 * args.padding - (rows - 1) * args.gap
    if usable_width <= 0 or usable_height <= 0:
        raise ValueError("padding/gap leave no room for tiles")
    cell_w = usable_width // args.columns
    cell_h = usable_height // rows
    shadow_margin = (
        args.shadow_blur * 3 + abs(args.shadow_offset_y)
        if args.shadow_blur and args.shadow_opacity
        else 0
    )
    effect_margin = args.outline * 2 + shadow_margin
    tile_area = (cell_w - effect_margin * 2, cell_h - effect_margin * 2)
    if tile_area[0] <= 0 or tile_area[1] <= 0:
        raise ValueError("cells are too small for the configured outline and shadow")

    for index, source in enumerate(sources):
        tile = ImageOps.contain(source, tile_area, Image.Resampling.LANCZOS)
        tile = finish_tile(tile, args)
        x = args.padding + (index % args.columns) * (cell_w + args.gap) + (cell_w - tile.width) // 2
        y = args.padding + (index // args.columns) * (cell_h + args.gap) + (cell_h - tile.height) // 2
        canvas.alpha_composite(tile, (x, y))


def save_canvas(canvas: Image.Image, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.suffix.lower() in {".jpg", ".jpeg"}:
        canvas.convert("RGB").save(output, quality=95)
    else:
        canvas.save(output)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", nargs="+", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--layout", choices=("stack", "grid"), default="stack")
    parser.add_argument("--width", type=int, default=1440)
    parser.add_argument("--height", type=int, default=2560)
    parser.add_argument("--background", type=parse_color, default=(255, 255, 255, 255))
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--tile-scale", type=float, default=0.46, help="Stack tile size as a fraction of canvas width")
    parser.add_argument("--rotation", type=float, default=16.0, help="Maximum absolute stack rotation in degrees")
    parser.add_argument("--outline", type=int, default=8, help="Gapless white outline grown directly from the cutout edge")
    parser.add_argument("--shadow-blur", type=int, default=14, help="Soft shadow blur radius in pixels")
    parser.add_argument("--shadow-offset-y", type=int, default=8, help="Downward shadow offset in pixels")
    parser.add_argument("--shadow-opacity", type=int, default=48, help="Shadow alpha from 0 to 255")
    parser.add_argument("--background-removal", choices=("auto", "never"), default="auto")
    parser.add_argument("--require-alpha", action="store_true", help="Reject opaque inputs that were not cut out")
    parser.add_argument("--columns", type=int, default=2)
    parser.add_argument("--gap", type=int, default=24)
    parser.add_argument("--padding", type=int, default=48)
    parser.add_argument("--overwrite", action="store_true", help="Allow replacing an existing output file")
    args = parser.parse_args()

    if args.width <= 0 or args.height <= 0 or args.columns <= 0:
        parser.error("width, height, and columns must be positive")
    if args.gap < 0 or args.padding < 0 or args.outline < 0 or args.shadow_blur < 0:
        parser.error("gap, padding, outline, and shadow blur must be non-negative")
    if args.outline > 100:
        parser.error("outline must not exceed 100 pixels")
    if args.shadow_blur > 100:
        parser.error("shadow blur must not exceed 100 pixels")
    if not -100 <= args.shadow_offset_y <= 100:
        parser.error("shadow offset must be between -100 and 100 pixels")
    if not 0 <= args.shadow_opacity <= 255:
        parser.error("shadow opacity must be between 0 and 255")
    if not 0.2 <= args.tile_scale <= 0.8:
        parser.error("tile-scale must be between 0.2 and 0.8")
    if not 0 <= args.rotation <= 30:
        parser.error("rotation must be between 0 and 30 degrees")
    if len(args.input) > MAX_INPUTS:
        parser.error(f"at most {MAX_INPUTS} input images are allowed")
    if args.width * args.height > MAX_CANVAS_PIXELS:
        parser.error(f"canvas may contain at most {MAX_CANVAS_PIXELS:,} pixels")
    if args.output.exists() and not args.overwrite:
        parser.error("output already exists; pass --overwrite to replace it")

    remove_background = args.layout == "stack" and args.background_removal == "auto"
    try:
        sources = [prepare_cutout(path, remove_background, args.require_alpha) for path in args.input]
        canvas = Image.new("RGBA", (args.width, args.height), args.background)
        if args.layout == "stack":
            compose_stack(canvas, sources, args)
        else:
            compose_grid(canvas, sources, args)
        save_canvas(canvas, args.output)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    print(f"wrote {args.output} ({args.width}x{args.height}, {args.layout})")


if __name__ == "__main__":
    main()
