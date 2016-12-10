# -*- mode: python -*-
import os
from glob import glob

block_cipher = None


# Adding all css and images as part of additional resources
data_files_glob += glob(os.path.join('tiborcim', 'resources', 'images', '*.*'))
data_files = []
# Paths are a bit tricky: glob works on cwd (project root), pyinstaller relative
# starts on spec file location, and packed application relative starts on
# project root directory.
for x in data_files_glob:
    data_files += [(os.path.join('..', x), os.path.dirname(x))]

print('Spec file resources selected: %s' % data_files)


a = Analysis(['../run.py'],
             pathex=['../'],
             binaries=None,
             datas=data_files,
             hiddenimports = ['sip'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

pyz = PYZ(a.pure,
          a.zipped_data,
          cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Cim',
          strip=False,
          upx=True,
          # False hides the cli window, useful ON to debug
          console=False,
          debug=False,
          icon='package/icons/icon.ico')