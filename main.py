#!/usr/bin/env python3
"""Entrypoint for news-image-20261124 v3 (Builder A).

Stdlib only. The image is drawn at build time by render.py and shipped
as entry.png; this program only copies it into the grader's output
directory and sets mode 0644. Deterministic: both runs write the
same bytes.
"""
import os
import shutil


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, dst)
    # Verify the copy is complete: same size as the bundled image and
    # a PNG (first bytes are the PNG signature). A short copy must fail
    # loudly instead of being graded as a broken image.
    with open(dst, "rb") as fh:
        head = fh.read(8)
    if head != b"\x89PNG\r\n\x1a\n":
        raise ValueError("copied entry.png is not a PNG")
    if os.path.getsize(dst) != os.path.getsize(src):
        raise ValueError("copied entry.png size differs from bundled file")
    os.chmod(dst, 0o644)


if __name__ == "__main__":
    main()
