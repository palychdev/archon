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
