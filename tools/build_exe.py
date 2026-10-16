import PyInstaller.__main__


PyInstaller.__main__.run([
    "tools/entry.py",
    "--name", "archon",
    "--onefile",
    "--console",
    "--paths", "src",
])
