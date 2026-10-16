import PyInstaller.__main__


PyInstaller.__main__.run([
    "src/archon/__main__.py",
    "--name", "archon",
    "--onefile",
    "--console",
    "--paths", "src",
])
