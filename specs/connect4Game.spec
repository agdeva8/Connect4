# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['connect4Game.py'],
             pathex=['/home/Connect4'],
             binaries=[],
             datas=[ ( '/home/Connect4/icons/*.jpg', 'icons' ),
                      ( '/home/Connect4/fonts/*.ttf', 'fonts' )],
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
          [],
          exclude_binaries=True,
          name='connect4Game',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='connect4Game')
