#!/usr/bin/env python3
"""Build script for macOS app bundle using PyInstaller."""

import subprocess
import sys
from pathlib import Path


def main():
    """Build the macOS app."""
    project_root = Path(__file__).parent.parent
    src_dir = project_root / "src"

    # PyInstaller command
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--name=Background Remover",
        "--windowed",
        "--onedir",
        f"--add-data={src_dir / 'background_remover' / 'resources'}:resources",
        "--hidden-import=PIL",
        "--hidden-import=rembg",
        "--collect-all=rembg",
        "--collect-all=onnxruntime",
        str(src_dir / "background_remover" / "__main__.py"),
    ]

    print("Building macOS app...")
    print(f"Command: {' '.join(cmd)}")

    result = subprocess.run(cmd, cwd=project_root)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
