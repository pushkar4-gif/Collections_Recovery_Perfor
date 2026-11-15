"""Backward-compatible entry point for rebuilding the golden layer.
Run from any working directory: python src/build_golden.py
"""
from pathlib import Path
import runpy

if __name__ == "__main__":
    runpy.run_path(str(Path(__file__).with_name("build_analysis.py")), run_name="__main__")
