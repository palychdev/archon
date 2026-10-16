def run_menu() -> int:
    from .config import ScanConfig
    from .report import render
    from .scanner import has_engine, engine_hint, scan
    from .yarasc import match_file
    from .scanner import Hit
    from .entropy import is_packed
    from .hashes import walk_files

    if not has_engine():
        print(engine_hint())
        return 2
    root = input("path to scan: ").strip().strip('"')
    if not root:
        print("empty path")
        return 1
    yara = input("use yara? [y/N]: ").strip().lower() == "y"
    ent = input("check packed? [y/N]: ").strip().lower() == "y"
    cfg = ScanConfig()
    hits = scan(root, cfg.max_depth, cfg.max_size_mb, cfg.timeout_sec, cfg.exclude)
    if yara:
        for fp in walk_files(root):
            for rule in match_file(fp):
                hits.append(Hit(fp, "", f"yara:{rule}"))
    if ent:
        for fp in walk_files(root):
            if is_packed(fp):
                hits.append(Hit(fp, "", "heuristic:high-entropy"))
    print(render(hits))
    input("press enter to close...")
    return 1 if hits else 0
