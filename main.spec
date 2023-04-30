import sys, os, shutil

block_cipher = None

site_packages = os.path.join(os.path.dirname(sys.executable), "Lib", "site-packages")
added_files = []
working_dir_files = [
                ('assets', 'assets')
                ]

print('ADDED FILES: (will show up in sys._MEIPASS)')
print(added_files)
print('Copying files to the dist folder')

print(os.getcwd())
for tup in working_dir_files:
        print(tup)
        to_path = os.path.join(DISTPATH, tup[1])
        if os.path.exists(to_path):
                if os.path.isdir(to_path):
                        shutil.rmtree(to_path)
                else:
                        os.remove(to_path)
        if os.path.isdir(tup[0]):
                shutil.copytree(tup[0], to_path)
        else:
                shutil.copyfile(tup[0], to_path)

#### ... The rest of the spec file
a = Analysis(['main.py'],
             pathex=[],
             binaries=[],
             datas=added_files,
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
          name='Drifty Delivery Service',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False)
