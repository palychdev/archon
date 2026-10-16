import os
import time


def poll(folder: str, interval: int = 5):
    seen = set()
    for dp, _, fns in os.walk(folder):
        for fn in fns:
            seen.add(os.path.join(dp, fn))
    while True:
        time.sleep(interval)
        cur = set()
        for dp, _, fns in os.walk(folder):
            for fn in fns:
                cur.add(os.path.join(dp, fn))
        new = sorted(cur - seen)
        if new:
            return new
        seen = cur
