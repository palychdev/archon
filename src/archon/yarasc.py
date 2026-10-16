import os
import shutil
import subprocess


def _via_lib(path: str, rules_dir: str) -> list[str]:
    try:
        import yara
    except ImportError:
        return []
    hits: list[str] = []
    for fn in sorted(os.listdir(rules_dir)):
        if not fn.endswith(".rules"):
            continue
        rp = os.path.join(rules_dir, fn)
        try:
            rules = yara.compile(filepath=rp)
            m = rules.match(filepath=path)
            hits.extend([str(x) for x in m])
        except Exception:
            continue
    return hits


def _via_bin(path: str, rules_dir: str) -> list[str]:
    if shutil.which("yara") is None:
        return []
    hits: list[str] = []
    for fn in sorted(os.listdir(rules_dir)):
        if not fn.endswith(".rules"):
            continue
        rp = os.path.join(rules_dir, fn)
        p = subprocess.run(["yara", rp, path], capture_output=True, text=True, timeout=60)
        for line in (p.stdout or "").splitlines():
            name = line.split(" ", 1)[0].strip()
            if name:
                hits.append(name)
    return hits


def match_file(path: str, rules_dir: str = "rules") -> list[str]:
    if not os.path.isfile(path) or not os.path.isdir(rules_dir):
        return []
    hits = _via_lib(path, rules_dir)
    if hits:
        return hits
    return _via_bin(path, rules_dir)
