#!/usr/bin/env python3
"""Superseded. The legal pages are now built together with every other page by tools/build-pages.py
(their wording lives in tools/legal_text.py). This shim just runs the new builder."""
import pathlib, runpy
runpy.run_path(str(pathlib.Path(__file__).resolve().parent / "build-pages.py"), run_name="__main__")
