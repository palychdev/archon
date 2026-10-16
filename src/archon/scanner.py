import shutil
import subprocess
from dataclasses import dataclass


@dataclass
class Hit:
    path: str
    inner: str
    sig: str


def has_engine() -> bool:
    return shutil.which("clamscan") is not None


def build_args(path: str, depth: int, max_mb: int, exclude: tuple[str, ...] = ()) -> list[str]:
    args = [
        "clamscan",
        "-r",
        f"--max-filesize={max_mb}M",
        f"--max-scansize={max_mb}M",
        f"--max-recursion={depth}",
        "--scan-archive=yes",
    ]
    for e in exclude:
        args.append(f"--exclude-dir={e}")
    args.append(path)
    return args


def parse_line(line: str) -> Hit | None:
    if "FOUND" not in line:
        return None
    left, _, sig = line.rpartition("FOUND")
    left = left.strip().rstrip(":")
    sig = sig.strip()
    if "!" in left:
        outer, _, inner = left.partition("!")
        return Hit(outer.strip(), inner.strip("() "), sig)
    return Hit(left, "", sig)


def scan(path: str, depth: int = 5, max_mb: int = 512, timeout_sec: int = 600, exclude: tuple[str, ...] = ()) -> list[Hit]:
    if not has_engine():
        return []
    try:
        p = subprocess.run(build_args(path, depth, max_mb, exclude), capture_output=True, text=True, timeout=timeout_sec)
    except subprocess.TimeoutExpired:
        return [Hit(path, "", "ScanTimeout")]
    out = (p.stdout or "") + "\n" + (p.stderr or "")
    hits: list[Hit] = []
    for line in out.splitlines():
        h = parse_line(line)
        if h:
            hits.append(h)
    return hits
