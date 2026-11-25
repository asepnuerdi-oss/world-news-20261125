#!/usr/bin/env python3
"""make.fun entry — 'Sum up 25 November's world news in one image'.

Writes the bundled front-page artwork to /output/entry.png.
Pure standard library, no network, fully deterministic: the output is a
byte-for-byte copy of the image stored in this repository, so two runs
always produce identical bytes.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "world-news-2026-11-25.png")
OUTPUT = os.path.join("/output", "entry.png")


def main():
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    shutil.copyfile(SOURCE, OUTPUT)
    print("wrote", OUTPUT, os.path.getsize(OUTPUT), "bytes")


if __name__ == "__main__":
    main()
