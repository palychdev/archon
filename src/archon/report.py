from .scanner import Hit


def render(hits: list[Hit]) -> str:
    if not hits:
        return "clean, nothing found"
    rows = ["path | inner | sig"]
    for h in hits:
        rows.append(f"{h.path} | {h.inner or '-'} | {h.sig}")
    return "\n".join(rows)
