import os
import shutil
import subprocess


def ensure_user_conf() -> str:
    base = os.environ.get("APPDATA", os.path.expanduser("~"))
    d = os.path.join(base, "archon")
    os.makedirs(os.path.join(d, "db"), exist_ok=True)
    dst = os.path.join(d, "freshclam.conf")
    if os.path.isfile(dst):
        return dst
    src = r"C:\Program Files\ClamAV\conf_examples\freshclam.conf.sample"
    if not os.path.isfile(src):
        return dst
    with open(src, encoding="utf-8", errors="ignore") as f:
        lines = [l for l in f if not l.startswith("Example")]
    db = os.path.join(d, "db").replace("\\", "/")
    lines.append(f'\nDatabaseDirectory "{db}"\n')
    with open(dst, "w", encoding="utf-8") as f:
        f.writelines(lines)
    return dst


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
    ensure_user_conf()
    if shutil.which("clamscan") is None:
        print("installed but no clamscan in PATH, reopen terminal and run archon --update")
        return 3
    from .update import update
    return update()
