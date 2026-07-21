#!/usr/bin/env python3
"""Deterministic post-processing for 2D game asset sheets."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from PIL import Image
import numpy as np


@dataclass
class FrameRecord:
    index: int
    row: int
    col: int
    bbox: tuple[int, int, int, int] | None
    source_size: tuple[int, int]
    trimmed_size: tuple[int, int]
    aligned_size: tuple[int, int]
    edge_touch: bool
    exported: bool


def parse_hex_color(value: str) -> tuple[int, int, int]:
    cleaned = value.strip().lower().replace("#", "")
    if len(cleaned) != 6:
        raise ValueError(f"Invalid RGB hex color: {value}")
    return tuple(int(cleaned[i : i + 2], 16) for i in range(0, 6, 2))


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def load_rgba(path: Path) -> Image.Image:
    return Image.open(path).convert("RGBA")


def apply_chroma_key(image: Image.Image, rgb: tuple[int, int, int], tolerance: int) -> Image.Image:
    output = image.copy()
    pixels = output.load()
    width, height = output.size
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            if (
                abs(r - rgb[0]) <= tolerance
                and abs(g - rgb[1]) <= tolerance
                and abs(b - rgb[2]) <= tolerance
            ):
                pixels[x, y] = (r, g, b, 0)
            else:
                pixels[x, y] = (r, g, b, a)
    return output


def split_grid(image: Image.Image, rows: int, cols: int) -> list[tuple[int, int, int, int, Image.Image]]:
    cell_w = image.width // cols
    cell_h = image.height // rows
    frames: list[tuple[int, int, int, int, Image.Image]] = []
    for row in range(rows):
        for col in range(cols):
            left = col * cell_w
            top = row * cell_h
            box = (left, top, left + cell_w, top + cell_h)
            frames.append((row, col, cell_w, cell_h, image.crop(box)))
    return frames


def trim_transparent(image: Image.Image) -> tuple[Image.Image | None, tuple[int, int, int, int] | None]:
    bbox = image.getbbox()
    if bbox is None:
        return None, None
    return image.crop(bbox), bbox


def connected_component_boxes(
    image: Image.Image,
    min_component_area: int,
    padding: int,
) -> list[tuple[int, int, int, int]]:
    alpha = np.array(image.getchannel("A"))
    mask = alpha > 0
    height, width = mask.shape
    visited = np.zeros_like(mask, dtype=bool)
    boxes: list[tuple[int, int, int, int]] = []

    for y in range(height):
        for x in range(width):
            if not mask[y, x] or visited[y, x]:
                continue
            stack = [(x, y)]
            visited[y, x] = True
            min_x = max_x = x
            min_y = max_y = y
            area = 0

            while stack:
                cx, cy = stack.pop()
                area += 1
                min_x = min(min_x, cx)
                min_y = min(min_y, cy)
                max_x = max(max_x, cx)
                max_y = max(max_y, cy)
                for nx, ny in ((cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1)):
                    if 0 <= nx < width and 0 <= ny < height and mask[ny, nx] and not visited[ny, nx]:
                        visited[ny, nx] = True
                        stack.append((nx, ny))

            if area < min_component_area:
                continue
            left = max(0, min_x - padding)
            top = max(0, min_y - padding)
            right = min(width, max_x + 1 + padding)
            bottom = min(height, max_y + 1 + padding)
            boxes.append((left, top, right, bottom))
    return boxes


def select_component_region(
    image: Image.Image,
    mode: str,
    min_component_area: int,
    padding: int,
) -> tuple[Image.Image | None, tuple[int, int, int, int] | None]:
    boxes = connected_component_boxes(image, min_component_area, padding)
    if not boxes:
        return trim_transparent(image)
    if mode == "largest":
        boxes.sort(key=lambda box: (box[2] - box[0]) * (box[3] - box[1]), reverse=True)
        selected = boxes[0]
    else:
        selected = (
            min(box[0] for box in boxes),
            min(box[1] for box in boxes),
            max(box[2] for box in boxes),
            max(box[3] for box in boxes),
        )
    return image.crop(selected), selected


def bbox_touches_edge(bbox: tuple[int, int, int, int] | None, source_size: tuple[int, int]) -> bool:
    if bbox is None:
        return False
    left, top, right, bottom = bbox
    width, height = source_size
    return left == 0 or top == 0 or right == width or bottom == height


def compute_canvas_size(images: Iterable[Image.Image]) -> tuple[int, int]:
    widths = [image.width for image in images]
    heights = [image.height for image in images]
    return (max(widths, default=1), max(heights, default=1))


def align_frame(image: Image.Image, canvas_size: tuple[int, int], anchor: str) -> Image.Image:
    canvas = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
    if anchor == "bottom":
        x = (canvas.width - image.width) // 2
        y = canvas.height - image.height
    else:
        x = (canvas.width - image.width) // 2
        y = (canvas.height - image.height) // 2
    canvas.alpha_composite(image, (x, y))
    return canvas


def save_aligned_sheet(
    images: list[Image.Image],
    rows: int,
    cols: int,
    sheet_path: Path,
) -> None:
    if not images:
        return
    cell_w, cell_h = images[0].size
    sheet = Image.new("RGBA", (cell_w * cols, cell_h * rows), (0, 0, 0, 0))
    for index, image in enumerate(images):
        row = index // cols
        col = index % cols
        sheet.alpha_composite(image, (col * cell_w, row * cell_h))
    sheet.save(sheet_path)


def save_gif(images: list[Image.Image], gif_path: Path, duration_ms: int) -> None:
    if not images:
        return
    images[0].save(
        gif_path,
        save_all=True,
        append_images=images[1:],
        duration=duration_ms,
        loop=0,
        disposal=2,
        transparency=0,
    )


def run_sprite_mode(args: argparse.Namespace) -> None:
    output_dir = Path(args.output_dir).resolve()
    frames_dir = output_dir / "frames"
    ensure_dir(frames_dir)

    image = load_rgba(Path(args.input).resolve())
    if args.chroma_key:
        image = apply_chroma_key(image, parse_hex_color(args.chroma_key), args.tolerance)

    raw_frames = split_grid(image, args.rows, args.cols)
    trimmed_images: list[Image.Image] = []
    records: list[FrameRecord] = []

    for index, (row, col, cell_w, cell_h, frame) in enumerate(raw_frames):
        trimmed, bbox = select_component_region(
            frame,
            mode=args.component_mode,
            min_component_area=args.min_component_area,
            padding=args.component_padding,
        )
        exported = trimmed is not None
        if trimmed is not None:
            trimmed_images.append(trimmed)
        records.append(
            FrameRecord(
                index=index,
                row=row,
                col=col,
                bbox=bbox,
                source_size=(cell_w, cell_h),
                trimmed_size=(trimmed.width, trimmed.height) if trimmed is not None else (0, 0),
                aligned_size=(0, 0),
                edge_touch=bbox_touches_edge(bbox, (cell_w, cell_h)),
                exported=exported,
            )
        )

    canvas_size = compute_canvas_size(trimmed_images)
    aligned_images: list[Image.Image] = []

    trimmed_iter = iter(trimmed_images)
    for record in records:
        if not record.exported:
            continue
        trimmed = next(trimmed_iter)
        aligned = align_frame(trimmed, canvas_size, args.anchor)
        aligned_images.append(aligned)
        record.aligned_size = aligned.size
        aligned.save(frames_dir / f"frame_{record.index:03d}.png")

    sheet_rows = args.rows if args.keep_grid else 1
    sheet_cols = args.cols if args.keep_grid else max(1, len(aligned_images))
    if args.keep_grid:
        sheet_images: list[Image.Image] = []
        aligned_iter = iter(aligned_images)
        for record in records:
            if record.exported:
                sheet_images.append(next(aligned_iter))
            else:
                sheet_images.append(Image.new("RGBA", canvas_size, (0, 0, 0, 0)))
    else:
        sheet_images = aligned_images

    save_aligned_sheet(sheet_images, sheet_rows, sheet_cols, output_dir / "sheet_aligned.png")
    if args.gif:
        save_gif(aligned_images, output_dir / "preview.gif", args.gif_duration)

    metadata = {
        "mode": "sprite",
        "input": str(Path(args.input).resolve()),
        "rows": args.rows,
        "cols": args.cols,
        "anchor": args.anchor,
        "frame_count": len(records),
        "non_empty_frames": sum(1 for record in records if record.exported),
        "max_content_width": canvas_size[0],
        "max_content_height": canvas_size[1],
        "edge_touch_frames": [record.index for record in records if record.edge_touch],
        "frames": [record.__dict__ for record in records],
    }
    (output_dir / "qa.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")


def run_prop_pack_mode(args: argparse.Namespace) -> None:
    output_dir = Path(args.output_dir).resolve()
    props_dir = output_dir / "props"
    ensure_dir(props_dir)

    image = load_rgba(Path(args.input).resolve())
    if args.chroma_key:
        image = apply_chroma_key(image, parse_hex_color(args.chroma_key), args.tolerance)

    raw_frames = split_grid(image, args.rows, args.cols)
    exported = 0
    records: list[FrameRecord] = []

    for index, (row, col, cell_w, cell_h, frame) in enumerate(raw_frames):
        trimmed, bbox = trim_transparent(frame)
        has_content = trimmed is not None
        if has_content:
            exported += 1
            trimmed.save(props_dir / f"prop_{index:03d}.png")
        records.append(
            FrameRecord(
                index=index,
                row=row,
                col=col,
                bbox=bbox,
                source_size=(cell_w, cell_h),
                trimmed_size=(trimmed.width, trimmed.height) if trimmed is not None else (0, 0),
                aligned_size=(trimmed.width, trimmed.height) if trimmed is not None else (0, 0),
                edge_touch=bbox_touches_edge(bbox, (cell_w, cell_h)),
                exported=has_content,
            )
        )

    metadata = {
        "mode": "prop-pack",
        "input": str(Path(args.input).resolve()),
        "rows": args.rows,
        "cols": args.cols,
        "exported_props": exported,
        "edge_touch_frames": [record.index for record in records if record.edge_touch],
        "frames": [record.__dict__ for record in records],
    }
    (output_dir / "qa.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Post-process 2D sprite sheets and prop packs.")
    subparsers = parser.add_subparsers(dest="mode", required=True)

    sprite = subparsers.add_parser("sprite", help="Slice and align an animation sheet.")
    sprite.add_argument("--input", required=True, help="Input sheet path.")
    sprite.add_argument("--output-dir", required=True, help="Output directory.")
    sprite.add_argument("--rows", required=True, type=int, help="Grid rows.")
    sprite.add_argument("--cols", required=True, type=int, help="Grid cols.")
    sprite.add_argument("--anchor", choices=("center", "bottom"), default="center")
    sprite.add_argument("--chroma-key", default="", help="RGB hex color to remove, e.g. ff00ff.")
    sprite.add_argument("--tolerance", default=10, type=int, help="Chroma-key tolerance.")
    sprite.add_argument("--gif", action="store_true", help="Export preview.gif.")
    sprite.add_argument("--gif-duration", default=120, type=int, help="GIF frame duration in ms.")
    sprite.add_argument("--component-mode", choices=("all", "largest"), default="all")
    sprite.add_argument("--component-padding", default=0, type=int)
    sprite.add_argument("--min-component-area", default=4, type=int)
    sprite.add_argument(
        "--keep-grid",
        action="store_true",
        help="Keep the original rows/cols when rebuilding the aligned sheet.",
    )

    prop_pack = subparsers.add_parser("prop-pack", help="Slice a prop pack into individual PNG files.")
    prop_pack.add_argument("--input", required=True, help="Input pack path.")
    prop_pack.add_argument("--output-dir", required=True, help="Output directory.")
    prop_pack.add_argument("--rows", required=True, type=int, help="Grid rows.")
    prop_pack.add_argument("--cols", required=True, type=int, help="Grid cols.")
    prop_pack.add_argument("--chroma-key", default="", help="RGB hex color to remove, e.g. ff00ff.")
    prop_pack.add_argument("--tolerance", default=10, type=int, help="Chroma-key tolerance.")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if args.mode == "sprite":
        run_sprite_mode(args)
    else:
        run_prop_pack_mode(args)


if __name__ == "__main__":
    main()
