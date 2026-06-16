#!/usr/bin/env python3
"""CLI entry point for the annotated screenshot test framework.

Usage:
    python run_test.py --url https://example.com --steps example_steps.py
    python run_test.py --steps example_steps.py
"""
import argparse
import importlib.util
import sys
from pathlib import Path

from engine import AnnotatedBrowser


def load_steps_module(path: str):
    """Dynamically load a steps file as a module."""
    spec = importlib.util.spec_from_file_location("steps", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    parser = argparse.ArgumentParser(description="Run annotated UI tests")
    parser.add_argument("--steps", required=True, help="Path to steps file (Python module with a run(browser) function)")
    parser.add_argument("--output", default=None, help="Output directory for screenshots (default: reports/)")
    parser.add_argument("--headed", action="store_true", help="Run with visible browser window")
    args = parser.parse_args()

    # Override headless if --headed is passed
    if args.headed:
        import config
        config.HEADLESS = False

    steps_mod = load_steps_module(args.steps)

    if not hasattr(steps_mod, "run"):
        print(f"Error: {args.steps} must define a run(browser) function.")
        sys.exit(1)

    print(f"🎬 Starting test run...")
    print(f"   Steps: {args.steps}")
    print(f"   Output: {args.output or 'reports/'}")
    print()

    with AnnotatedBrowser(output_dir=args.output) as browser:
        steps_mod.run(browser)

    print(f"\n✅ Done! {browser.step} screenshots saved to {browser.output_dir}/")


if __name__ == "__main__":
    main()
