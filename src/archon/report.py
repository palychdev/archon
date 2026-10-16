import json
from .scanner import Hit


def render(hits: list[Hit]) -> str:
    if not hits:
        return "clean, nothing found"
    rows = ["path | inner | sig"]
    for h in hits:
        rows.append(f"{h.path} | {h.inner or '-'} | {h.sig}")
    return "\n".join(rows)


def render_json(hits: list[Hit]) -> str:
    data = [{"path": h.path, "inner": h.inner, "sig": h.sig} for h in hits]
    return json.dumps(data, ensure_ascii=False, indent=2)
