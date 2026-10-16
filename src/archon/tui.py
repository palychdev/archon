import sys


def progress(i: int, total: int, label: str = "") -> None:
    pct = int(i * 100 / max(1, total))
    bar = "#" * (pct // 5) + "-" * (20 - pct // 5)
    sys.stdout.write(f"\r[{bar}] {pct}% {label}")
    sys.stdout.flush()
    if i >= total:
        print()
