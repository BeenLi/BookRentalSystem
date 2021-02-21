# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['租书系统.py'],
             pathex=['C:\\Users\\wanli\\Desktop\\项目文档\\3_租书系统\\BookRentalSystem'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='租书系统',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , icon='C:\\Users\\wanli\\Desktop\\项目文档\\3_租书系统\\BookRentalSystem\\reading-book.ico')
