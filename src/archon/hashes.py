import hashlib
import os


def sha256_of(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def walk_files(root: str) -> list[str]:
    if os.path.isfile(root):
        return [root]
    out: list[str] = []
    for dp, _, fns in os.walk(root):
        for fn in fns:
            out.append(os.path.join(dp, fn))
    return out
