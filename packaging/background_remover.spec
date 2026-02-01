# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec file for Background Remover."""

import sys
from pathlib import Path

block_cipher = None

# Determine platform-specific settings
is_macos = sys.platform == 'darwin'
is_windows = sys.platform == 'win32'

project_root = Path(SPECPATH).parent
src_dir = project_root / 'src'

a = Analysis(
    [str(src_dir / 'background_remover' / '__main__.py')],
    pathex=[str(src_dir)],
    binaries=[],
    datas=[
        (str(src_dir / 'background_remover' / 'resources'), 'resources'),
    ],
    hiddenimports=[
        'PIL',
        'rembg',
        'onnxruntime',
    ],
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
