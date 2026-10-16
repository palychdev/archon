import math
import os


def shannon(path: str) -> float:
    try:
        with open(path, "rb") as f:
            data = f.read(1024 * 1024)
    except OSError:
        return 0.0
    if not data:
        return 0.0
    freq = [0] * 256
    for b in data:
        freq[b] += 1
    ent = 0.0
    n = len(data)
    for c in freq:
        if c:
            p = c / n
            ent -= p * math.log2(p)
    return ent


def is_packed(path: str, limit: float = 7.5) -> bool:
    if not os.path.isfile(path):
        return False
    return shannon(path) >= limit
