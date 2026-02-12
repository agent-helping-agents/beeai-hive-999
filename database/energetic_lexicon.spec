# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller Spec File for Energetic Lexicon
🔒 PRIVATE - PROPRIETARY
© 2025 Baker Street Laboratory

Builds standalone executable with all dependencies bundled.
"""

import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# ============================================================================
# HIDDEN IMPORTS
# ============================================================================
# Packages that PyInstaller can't detect automatically

hidden_imports = [
    # Database
    'sqlalchemy.sql.default_comparator',
    'sqlalchemy.ext.declarative',
    'sqlalchemy.orm',

    # CLI & UI
    'typer',
    'rich',
    'rich.console',
    'rich.table',
    'rich.panel',
    'rich.progress',

    # Encryption
    'cryptography',
    'gnupg',

    # Future integrations (commented until implemented)
    # 'chromadb',
    # 'sentence_transformers',
    # 'transformers',
    # 'torch',
]

# ============================================================================
# DATA FILES
# ============================================================================
# Non-Python files that need to be bundled

datas = []

# Database schema
datas += [('schema.sql', '.')]

# Documentation
datas += [('README.md', '.')]
datas += [('SECURITY.md', '.')]

# Future: ML models (when ChromaDB integrated)
# datas += collect_data_files('sentence_transformers')
# datas += collect_data_files('transformers')
# datas += collect_data_files('chromadb')

# ============================================================================
# EXCLUDED MODULES
# ============================================================================
# Large packages we don't need (reduce size)

excludes = [
    # GUI frameworks
    'tkinter',
    'PyQt5',
    'PyQt6',
    'PySide2',
    'PySide6',

    # Scientific computing (not needed yet)
    'matplotlib',
    'scipy',
    'pandas',
    'numpy.distutils',

    # Jupyter
    'jupyter',
    'notebook',
    'IPython',

    # Testing
    'pytest',
    'unittest',

    # Documentation
    'sphinx',
]

# ============================================================================
# ANALYSIS
# ============================================================================

a = Analysis(
    ['src/cli_main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# ============================================================================
# PYZ (Compressed Python Archive)
# ============================================================================

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# ============================================================================
# EXE (Executable)
# ============================================================================

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='energetic-lexicon',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # UPX compression (reduces size by ~40%)
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # CLI application
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # icon='assets/icon.ico'  # Add icon when available
)
