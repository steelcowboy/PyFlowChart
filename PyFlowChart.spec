# -*- mode: python3 -*-

import os
import site

#gnome_path = os.path.join(site.getsitepackages()[1], 'gnome')
#typelib_path = os.path.join(gnome_path, 'lib', 'girepository-1.0')

gpath = os.path.join(site.getsitepackages()[1], 'gnome')
tpath = os.path.join(gpath, 'lib', 'girepository-1.0')

missing_files = []

#for tl in ["GdkPixbuf-2.0.typelib", "GModule-2.0.typelib"] :
#    missing_files.append((os.path.join(typelib_path, tl), "./gi_typelibs"))

for tl in os.listdir(tpath):
     missing_files.append((os.path.join(tpath, tl), "./gi_typelibs"))


#for dll in ["liblcms2-2.dll"] :
#    missing_files.append((os.path.join(gnome_path, dll), "./"))

excluded = [("./share/*.*"), ("./share/etc/*.*")]

block_cipher = None


a = Analysis(['pyflowchart\main.py'],
             pathex=['C:\\Users\\Jim Heald\\projects\\PyFlowChart\\pyflowchart'],
             binaries=missing_files,            
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

"""
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='PyFlowChart',
          debug=False,
          strip=False,
          upx=True,
          console=True )
"""
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='PyFlowChart',
          debug=False,
          strip=False,
          upx=True,
          console=True)
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='PyFlowChart')

