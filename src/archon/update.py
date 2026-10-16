import shutil
import subprocess


def has_updater() -> bool:
    return shutil.which("freshclam") is not None


def update(unofficial: bool = False) -> int:
    if not has_updater():
        print("no freshclam found")
        return 2
    p = subprocess.run(["freshclam"], capture_output=True, text=True)
    print((p.stdout or "")[-2000:])
    if unofficial:
        up = shutil.which("clamav-unofficial-sigs.sh")
        if not up:
            print("no unofficial sigs tool, skipping")
            return p.returncode
        q = subprocess.run([up], capture_output=True, text=True)
        print((q.stdout or "")[-2000:])
        return q.returncode
    return p.returncode
