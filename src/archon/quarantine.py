import os
import shutil


def quarantine_hits(paths: list[str], qdir: str) -> list[str]:
    os.makedirs(qdir, exist_ok=True)
    moved: list[str] = []
    for p in paths:
        if not os.path.isfile(p):
            continue
        dst = os.path.join(qdir, os.path.basename(p))
        try:
            shutil.move(p, dst)
            moved.append(dst)
        except OSError:
            continue
    return moved


def restore(qdir: str, outdir: str) -> list[str]:
    os.makedirs(outdir, exist_ok=True)
    back: list[str] = []
    if not os.path.isdir(qdir):
        return back
    for fn in sorted(os.listdir(qdir)):
        src = os.path.join(qdir, fn)
        dst = os.path.join(outdir, fn)
        try:
            shutil.move(src, dst)
            back.append(dst)
        except OSError:
            continue
    return back
