#!/usr/bin/env python3
"""Create layout-only guide images for sheets and prop packs."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a layout-only guide image.")
    parser.add_argument("--rows", required=True, type=int)
    parser.add_argument("--cols", required=True, type=int)
    parser.add_argument("--cell-width", required=True, type=int)
    parser.add_argument("--cell-height", required=True, type=int)
    parser.add_argument("--output", required=True)
    parser.add_argument("--margin", default=12, type=int)
    parser.add_argument("--bg", default="ff00ff")
    parser.add_argument("--line", default="ffffff")
    return parser.parse_args()


def hex_to_rgb(value: str) -> tuple[int, int, int]:
    cleaned = value.strip().lower().replace("#", "")
    if len(cleaned) != 6:
        raise ValueError(f"Invalid hex color: {value}")
    return tuple(int(cleaned[i : i + 2], 16) for i in range(0, 6, 2))


def main() -> None:
    args = parse_args()
    width = args.cols * args.cell_width
    height = args.rows * args.cell_height
    image = Image.new("RGB", (width, height), hex_to_rgb(args.bg))
    draw = ImageDraw.Draw(image)
    line = hex_to_rgb(args.line)

    for row in range(args.rows):
        for col in range(args.cols):
            left = col * args.cell_width
            top = row * args.cell_height
            right = left + args.cell_width - 1
            bottom = top + args.cell_height - 1
            draw.rectangle((left, top, right, bottom), outline=line, width=1)
            inner_left = left + args.margin
            inner_top = top + args.margin
            inner_right = right - args.margin
            inner_bottom = bottom - args.margin
            if inner_right > inner_left and inner_bottom > inner_top:
                draw.rectangle((inner_left, inner_top, inner_right, inner_bottom), outline=line, width=1)

    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output)


if __name__ == "__main__":
    main()
