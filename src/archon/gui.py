import tkinter as tk
from tkinter import filedialog, messagebox


def run_gui() -> None:
    from .config import ScanConfig
    from .report import render
    from .scanner import has_engine, engine_hint, scan
    from .scanner import Hit
    from .yarasc import match_file
    from .entropy import is_packed
    from .hashes import walk_files

    win = tk.Tk()
    win.title("archon")
    win.geometry("560x420")

    path_var = tk.StringVar()
    yara_var = tk.BooleanVar()
    ent_var = tk.BooleanVar()
    out = tk.Text(win, height=18)
    out.pack(fill="both", expand=True, padx=8, pady=8)

    def pick():
        d = filedialog.askdirectory()
        if d:
            path_var.set(d)

    def go():
        if not has_engine():
            messagebox.showerror("archon", engine_hint())
            return
        root = path_var.get().strip()
        if not root:
            messagebox.showwarning("archon", "pick a folder first")
            return
        cfg = ScanConfig()
        hits = scan(root, cfg.max_depth, cfg.max_size_mb, cfg.timeout_sec, cfg.exclude)
        if yara_var.get():
            for fp in walk_files(root):
                for rule in match_file(fp):
                    hits.append(Hit(fp, "", f"yara:{rule}"))
        if ent_var.get():
            for fp in walk_files(root):
                if is_packed(fp):
                    hits.append(Hit(fp, "", "heuristic:high-entropy"))
        out.delete("1.0", "end")
        out.insert("end", render(hits))

    bar = tk.Frame(win)
    bar.pack(fill="x", padx=8)
    tk.Entry(bar, textvariable=path_var).pack(side="left", fill="x", expand=True)
    tk.Button(bar, text="...", command=pick).pack(side="left")
    tk.Button(bar, text="scan", command=go).pack(side="left", padx=4)

    opts = tk.Frame(win)
    opts.pack(fill="x", padx=8)
    tk.Checkbutton(opts, text="yara", variable=yara_var).pack(side="left")
    tk.Checkbutton(opts, text="packed", variable=ent_var).pack(side="left")

    win.mainloop()
