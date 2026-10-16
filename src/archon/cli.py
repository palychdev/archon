import argparse
from . import __version__


def main() -> int:
    p = argparse.ArgumentParser(prog="archon")
    p.add_argument("--version", action="store_true")
    p.add_argument("path", nargs="?")
    a = p.parse_args()
    if a.version:
        print(__version__)
        return 0
    print("archon 0.1.0 skeleton, engine next")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
