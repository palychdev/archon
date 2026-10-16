import shutil
import subprocess


def has_updater() -> bool:
    return shutil.which("freshclam") is not None


def update() -> int:
    if not has_updater():
        print("no freshclam found")
        return 2
    p = subprocess.run(["freshclam"], capture_output=True, text=True)
    print((p.stdout or "")[-2000:])
    return p.returncode
