#!/usr/bin/env python3
"""Compose a QA preview from a base map and separately placed prop PNG files."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compose a layered QA preview image.")
    parser.add_argument("--base", required=True, help="Base map PNG.")
    parser.add_argument("--layout", required=True, help="Layout JSON containing prop placements.")
    parser.add_argument("--output", required=True, help="Output preview PNG.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    base_path = Path(args.base).resolve()
    layout_path = Path(args.layout).resolve()
    output_path = Path(args.output).resolve()

    base = Image.open(base_path).convert("RGBA")
    layout = json.loads(layout_path.read_text(encoding="utf-8"))
    props = layout.get("props", [])

    canvas = base.copy()
    for prop in props:
        image_path = Path(prop["image"]).resolve()
        image = Image.open(image_path).convert("RGBA")
        x = int(prop.get("x", 0))
        y = int(prop.get("y", 0))
        canvas.alpha_composite(image, (x, y))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output_path)


if __name__ == "__main__":
    main()
