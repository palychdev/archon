import shutil
import subprocess


def setup() -> int:
    if shutil.which("clamscan") is not None:
        print("clamscan already here")
        return 0
    if shutil.which("winget") is None:
        print("no winget, install clamav by hand from clamav.net")
        return 2
    print("installing clamav via winget...")
    p = subprocess.run(["winget", "install", "-e", "--id", "Cisco.ClamAV", "--accept-source-agreements", "--accept-package-agreements"])
    if p.returncode != 0:
        print("winget failed, install by hand")
        return p.returncode
    if shutil.which("clamscan") is None:
        print("installed but no clamscan in PATH, reopen terminal and run archon --update")
        return 3
    from .update import update
    return update()
