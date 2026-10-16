import argparse
from . import __version__
from .config import ScanConfig
from .report import render
from .scanner import has_engine, scan
from .autoruns import list_run_keys, list_startup


def main() -> int:
    p = argparse.ArgumentParser(prog="archon")
    p.add_argument("--version", action="store_true")
    p.add_argument("--depth", type=int, default=5)
    p.add_argument("--max-mb", type=int, default=512)
    p.add_argument("--autoruns", action="store_true")
    p.add_argument("path", nargs="?")
    a = p.parse_args()
    if a.version:
        print(__version__)
        return 0
    if a.autoruns:
        for line in list_run_keys() + list_startup():
            print(line)
        return 0
    if not a.path:
        print("give me a path to scan")
        return 1
    if not has_engine():
        print("no clamscan found, install clamav first")
        return 2
    cfg = ScanConfig(max_depth=a.depth, max_size_mb=a.max_mb)
    hits = scan(a.path, cfg.max_depth, cfg.max_size_mb)
    print(render(hits))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
