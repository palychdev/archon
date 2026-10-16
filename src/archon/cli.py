import argparse
from . import __version__
from .config import ScanConfig
from .report import render, render_json
from .scanner import has_engine, scan
from .autoruns import list_run_keys, list_startup
from .hashes import sha256_of, walk_files


def main() -> int:
    p = argparse.ArgumentParser(prog="archon")
    p.add_argument("--version", action="store_true")
    p.add_argument("--depth", type=int, default=5)
    p.add_argument("--max-mb", type=int, default=512)
    p.add_argument("--autoruns", action="store_true")
    p.add_argument("--json", action="store_true")
    p.add_argument("--hashes", action="store_true")
    p.add_argument("--timeout", type=int, default=600)
    p.add_argument("--exclude", action="append", default=[])
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
    cfg = ScanConfig(max_depth=a.depth, max_size_mb=a.max_mb, timeout_sec=a.timeout, exclude=tuple(a.exclude))
    hits = scan(a.path, cfg.max_depth, cfg.max_size_mb, cfg.timeout_sec, cfg.exclude)
    if a.hashes:
        for fp in walk_files(a.path):
            try:
                print(f"{sha256_of(fp)}  {fp}")
            except OSError:
                continue
        return 0
    if a.json:
        print(render_json(hits))
    else:
        print(render(hits))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
