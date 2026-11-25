#!/usr/bin/env python3
"""Copy the bundled artwork to the entry output location.

This script takes the image file ``world-news-2026-11-25.png`` that lives
next to it and places an identical copy at ``/output/entry.png``. It
creates ``/output`` first when it is missing, so the copy always lands
where the entry is expected. Nothing is generated or changed here: the
output is simply the same file, byte for byte.
"""

import os
import shutil

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(SCRIPT_DIR, "world-news-2026-11-25.png")
DESTINATION = os.path.join("/output", "entry.png")


def main():
    os.makedirs(os.path.dirname(DESTINATION), exist_ok=True)
    shutil.copyfile(SOURCE, DESTINATION)
    size = os.path.getsize(DESTINATION)
    print(f"wrote {DESTINATION} ({size} bytes)")


if __name__ == "__main__":
    main()
