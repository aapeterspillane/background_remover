# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec file for Background Remover.

This is the single source of truth for PyInstaller configuration.
Used by both local builds and GitHub Actions CI.
"""

import sys
from pathlib import Path

from PyInstaller.utils.hooks import collect_all

block_cipher = None

# Determine platform-specific settings
is_macos = sys.platform == 'darwin'
is_windows = sys.platform == 'win32'

project_root = Path(SPECPATH).parent
src_dir = project_root / 'src'

# Collect all data files and binaries for packages that need them
datas = []
binaries = []
hiddenimports = []

# Packages that need full collection (data files, binaries, submodules)
collect_all_packages = ['rembg', 'onnxruntime', 'pymatting', 'pooch', 'scipy', 'skimage']

for package in collect_all_packages:
    pkg_datas, pkg_binaries, pkg_hiddenimports = collect_all(package)
    datas += pkg_datas
    binaries += pkg_binaries
    hiddenimports += pkg_hiddenimports

# Additional hidden imports not caught by collect_all
hiddenimports += [
    # PIL/Pillow
    'PIL',
    'PIL._imaging',
    'PIL.Image',
    # numpy
    'numpy',
]

a = Analysis(
    [str(src_dir / 'background_remover' / '__main__.py')],
    pathex=[str(src_dir)],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

if is_macos:
    exe = EXE(
        pyz,
        a.scripts,
        [],
        exclude_binaries=True,
        name='Background Remover',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        console=False,
        disable_windowed_traceback=False,
        argv_emulation=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
    )
    coll = COLLECT(
        exe,
        a.binaries,
        a.zipfiles,
        a.datas,
        strip=False,
        upx=True,
        upx_exclude=[],
        name='Background Remover',
    )
    app = BUNDLE(
        coll,
        name='Background Remover.app',
        icon=None,  # Add .icns file path here
        bundle_identifier='com.backgroundremover.app',
    )
else:
    exe = EXE(
        pyz,
        a.scripts,
        [],
        exclude_binaries=True,
        name='BackgroundRemover',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        console=False,
        disable_windowed_traceback=False,
        argv_emulation=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
        icon=None,  # Add .ico file path here
    )
    coll = COLLECT(
        exe,
        a.binaries,
        a.zipfiles,
        a.datas,
        strip=False,
        upx=True,
        upx_exclude=[],
        name='BackgroundRemover',
    )
