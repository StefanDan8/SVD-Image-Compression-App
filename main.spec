# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['source\\main.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\40767\\Desktop\\SVD-image-compression\\Lib\\site-packages\\tkinterdnd2', 'tkinterdnd2/')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    Tree('..\\SVD-Image_Compression_App\\resources', prefix='resources\\'),
    a.datas,
    [],
    name='SVD Image Compression',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon = 'resources\\icon.ico'
)
