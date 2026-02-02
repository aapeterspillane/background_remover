#!/usr/bin/env python3
"""Build script for Windows executable using PyInstaller.

Uses the spec file at packaging/background_remover.spec as the
single source of truth for build configuration.
"""

import subprocess
import sys
from pathlib import Path


def main():
    """Build the Windows executable."""
    project_root = Path(__file__).parent.parent
    spec_file = project_root / "packaging" / "background_remover.spec"

    if not spec_file.exists():
        print(f"Error: Spec file not found at {spec_file}")
        sys.exit(1)

    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        str(spec_file),
    ]

    print("Building Windows executable...")
    print(f"Command: {' '.join(cmd)}")

    result = subprocess.run(cmd, cwd=project_root)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
