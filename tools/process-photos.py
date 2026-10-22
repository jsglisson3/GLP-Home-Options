#!/usr/bin/env python3
"""Prepares photos for the Our work page.

    python3 tools/process-photos.py [--slug NAME] photo.jpg [photo2.jpg ...]

For every photo it turns the picture upright (EXIF orientation), removes ALL metadata (camera, date, GPS location),
and writes
  images/work/<slug>.jpg      the large version (long edge at most 1600 px), shown in the photo viewer
  images/work/<slug>-sm.jpg   a small version (long edge 800 px) for the grid, only when the original is bigger than 1200 px
Then it prints the lines to paste into tools/gallery_data.py (the alt text and caption are left for you to write from
what the photo actually shows). The slug defaults to the file name in lower case with dashes; use --slug when you give
exactly one file and want a specific name.

Needs Pillow (pip install pillow). Facebook already strips metadata from the photos it serves; this makes sure of it for
every other source, and keeps the files small.
"""
import pathlib
import re
import sys

from PIL import Image, ImageOps

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "images" / "work"
LARGE, SMALL, NEEDS_SMALL = 1600, 800, 1200


def fit(im, long_edge):
    w, h = im.size
    if max(w, h) <= long_edge:
        return im
    s = long_edge / max(w, h)
    return im.resize((round(w * s), round(h * s)), Image.LANCZOS)


def save(im, path):
    # No exif / icc_profile arguments: Pillow then writes a bare JPEG with no metadata at all.
    quality = 90 if max(im.size) <= 1000 else 84   # small photos are already soft: do not squeeze them again
    im.save(path, "JPEG", quality=quality, optimize=True, progressive=True)


def main(argv):
    slug = None
    if argv[:1] == ["--slug"]:
        slug, argv = argv[1], argv[2:]
    if not argv or (slug and len(argv) != 1):
        sys.exit(__doc__)
    OUT.mkdir(parents=True, exist_ok=True)
    for src in argv:
        p = pathlib.Path(src)
        name = slug or re.sub(r"[^a-z0-9]+", "-", p.stem.lower()).strip("-")
        im = ImageOps.exif_transpose(Image.open(p)).convert("RGB")
        big = fit(im, LARGE)
        save(big, OUT / f"{name}.jpg")
        line = f'dict(group="building", img="images/work/{name}.jpg", alt="", caption=""),'
        if max(im.size) > NEEDS_SMALL:
            save(fit(im, SMALL), OUT / f"{name}-sm.jpg")
            line = f'dict(group="building", img="images/work/{name}-sm.jpg", full="images/work/{name}.jpg", alt="", caption=""),'
        print(f"{p.name}: {im.size[0]}x{im.size[1]} -> {big.size[0]}x{big.size[1]}")
        print("   ", line)


if __name__ == "__main__":
    main(sys.argv[1:])
