# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file for Compass CLI

block_cipher = None

a = Analysis(
    ['../python/compass/__main__.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('../python/compass/prompts/*.md', 'compass/prompts'),
        ('../python/compass/db/schema.sql', 'compass/db'),
    ],
    hiddenimports=[
        'compass.cli',
        'compass.config',
        'compass.vault',
        'compass.paths',
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

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='compass',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
