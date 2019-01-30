# -*- mode: python -*-

block_cipher = None


a = Analysis(['WallPaper.py'],
             pathex=['D:\\spyderProjects\\10_worm'],
             binaries=[],
             datas=[('bgpics/*.jpg', 'bgpics'),
                    ('mottos.json', '.'),
                    ('fonts/*.ttf', 'fonts'),
                    ("panda.ico", '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='WallPaper',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False,
          icon='panda.ico')
