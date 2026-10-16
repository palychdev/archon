import argparse
from . import __version__
from .config import ScanConfig
from .report import render, render_json
from .scanner import has_engine, scan, engine_hint
from .autoruns import list_run_keys, list_startup, save_snapshot, diff_snapshot
from .hashes import sha256_of, walk_files
from .update import update
from .quarantine import quarantine_hits, restore
from .yarasc import match_file
from .cfgfile import load_toml
from .scanner import Hit
from .entropy import is_packed
from .parallel import map_files
from .tui import progress


def main() -> int:
    p = argparse.ArgumentParser(prog="archon")
    p.add_argument("--version", action="store_true")
    p.add_argument("--depth", type=int, default=None)
    p.add_argument("--max-mb", type=int, default=None)
    p.add_argument("--autoruns", action="store_true")
    p.add_argument("--json", action="store_true")
    p.add_argument("--hashes", action="store_true")
    p.add_argument("--update", action="store_true")
    p.add_argument("--timeout", type=int, default=None)
    p.add_argument("--exclude", action="append", default=None)
    p.add_argument("--quarantine", default="")
    p.add_argument("--restore", default="")
    p.add_argument("--yara", action="store_true")
    p.add_argument("--entropy", action="store_true")
    p.add_argument("--unofficial", action="store_true")
    p.add_argument("--snap-save", default="")
    p.add_argument("--snap-diff", default="")
    p.add_argument("--config", default="archon.toml")
    p.add_argument("--log", default="")
    p.add_argument("--rescan", default="")
    p.add_argument("--watch", default="")
    p.add_argument("--tui", action="store_true")
    p.add_argument("--workers", type=int, default=8)
    p.add_argument("--menu", action="store_true")
    p.add_argument("--gui", action="store_true")
    p.add_argument("path", nargs="?")
    a = p.parse_args()
    if a.version:
        print(__version__)
        return 0
    if a.gui:
        from .gui import run_gui
        run_gui()
        return 0
    if a.menu:
        from .menu import run_menu
        return run_menu()
    if a.update:
        return update(a.unofficial)
    if a.snap_save:
        save_snapshot(a.snap_save)
        return 0
    if a.snap_diff:
        for line in diff_snapshot(a.snap_diff):
            print(line)
        return 0
    if a.restore:
        for dst in restore(a.path or ".", a.restore):
            print(f"restored {dst}")
        return 0
    if a.autoruns:
        for line in list_run_keys() + list_startup():
            print(line)
        return 0
    target = a.rescan or a.path
    if not target:
        print("give me a path to scan")
        return 1
    if not has_engine():
        print(engine_hint())
        return 2
    file_cfg = load_toml(a.config).get("scan", {})
    depth = a.depth if a.depth is not None else int(file_cfg.get("depth", 5))
    max_mb = a.max_mb if a.max_mb is not None else int(file_cfg.get("max_mb", 512))
    timeout = a.timeout if a.timeout is not None else int(file_cfg.get("timeout", 600))
    exclude = tuple(a.exclude) if a.exclude else tuple(file_cfg.get("exclude", []))
    allow = set(file_cfg.get("allow_sha256", []))
    use_yara = a.yara or bool(file_cfg.get("use_yara", False))
    log_file = a.log or str(file_cfg.get("log_file", ""))
    cfg = ScanConfig(max_depth=depth, max_size_mb=max_mb, timeout_sec=timeout, exclude=exclude)
    if a.watch:
        from .watch import poll
        print(f"watching {target}")
        for fp in poll(target):
            print(f"new: {fp}")
        return 0
    hits = scan(target, cfg.max_depth, cfg.max_size_mb, cfg.timeout_sec, cfg.exclude)
    files = walk_files(target)
    if use_yara:
        def _ym(fp: str):
            return [(fp, r) for r in match_file(fp)]
        for i, pairs in enumerate(map_files(_ym, files, a.workers), 1):
            if a.tui:
                progress(i, len(files), "yara")
            for fp, rule in pairs:
                hits.append(Hit(fp, "", f"yara:{rule}"))
    if a.entropy:
        def _em(fp: str):
            return (fp, is_packed(fp))
        for i, res in enumerate(map_files(_em, files, a.workers), 1):
            if a.tui:
                progress(i, len(files), "entropy")
            fp, packed = res
            if packed:
                hits.append(Hit(fp, "", "heuristic:high-entropy"))
    if allow:
        kept: list[Hit] = []
        for h in hits:
            try:
                digest = sha256_of(h.path) if h.path else ""
            except OSError:
                digest = ""
            if digest not in allow:
                kept.append(h)
        hits = kept
    if a.quarantine:
        paths = sorted({h.path for h in hits})
        for dst in quarantine_hits(paths, a.quarantine):
            print(f"moved {dst}")
        return 1 if hits else 0
    if a.hashes:
        for fp in walk_files(target):
            try:
                print(f"{sha256_of(fp)}  {fp}")
            except OSError:
                continue
        return 0
    if a.json:
        print(render_json(hits))
    else:
        print(render(hits))
    if log_file:
        try:
            with open(log_file, "a", encoding="utf-8") as f:
                f.write((render_json(hits) if a.json else render(hits)) + "\n")
        except OSError:
            pass
    return 1 if hits else 0


if __name__ == "__main__":
    raise SystemExit(main())
