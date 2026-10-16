import PyInstaller.__main__


PyInstaller.__main__.run([
    "src/archon/cli.py",
    "--name", "archon",
    "--onefile",
    "--console",
])
