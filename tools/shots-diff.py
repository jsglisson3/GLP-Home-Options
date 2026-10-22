#!/usr/bin/env python3
"""Compare two folders of screenshots made by tools/shots.py.

Usage:  python3 tools/shots-diff.py BEFORE_DIR AFTER_DIR
Prints one line per picture: identical, a changed-pixel percentage, or a size change. For every
picture that differs it also writes AFTER_DIR/diff/<name>.png (changed pixels in red over a faded copy).
Exit code 0 = every picture identical, 1 = something differs, 2 = a picture is missing.
A small tolerance (8 of 255 per color channel) ignores font anti-aliasing noise.
"""
import os
import sys

from PIL import Image, ImageChops

TOL = 8


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    a_dir, b_dir = sys.argv[1], sys.argv[2]
    names = sorted(n for n in os.listdir(a_dir) if n.endswith(".png"))
    if not names:
        print("no pictures in", a_dir)
        return 2
    worst = 0
    for n in names:
        pa, pb = os.path.join(a_dir, n), os.path.join(b_dir, n)
        if not os.path.exists(pb):
            print(f"{n:28s} MISSING in {b_dir}")
            worst = max(worst, 2)
            continue
        a, b = Image.open(pa).convert("RGB"), Image.open(pb).convert("RGB")
        if a.size != b.size:
            print(f"{n:28s} SIZE CHANGED {a.size[0]}x{a.size[1]} -> {b.size[0]}x{b.size[1]} (the page got {'taller' if b.size[1] > a.size[1] else 'shorter'})")
            worst = max(worst, 1)
            continue
        diff = ImageChops.difference(a, b).convert("L").point(lambda v: 255 if v > TOL else 0)
        box = diff.getbbox()
        if box is None:
            print(f"{n:28s} identical")
            continue
        changed = diff.histogram()[255] / (a.size[0] * a.size[1]) * 100
        print(f"{n:28s} {changed:.2f}% of pixels differ, in the area {box}")
        os.makedirs(os.path.join(b_dir, "diff"), exist_ok=True)
        faded = Image.blend(b, Image.new("RGB", b.size, (255, 255, 255)), 0.7)
        faded.paste(Image.new("RGB", b.size, (220, 30, 30)), mask=diff)
        faded.save(os.path.join(b_dir, "diff", n))
        worst = max(worst, 1)
    print("RESULT:", "every picture identical" if worst == 0 else "differences found (see the lines above)")
    return worst


if __name__ == "__main__":
    sys.exit(main())
