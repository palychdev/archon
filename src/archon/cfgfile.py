import os

try:
    import tomllib
except ModuleNotFoundError:
    tomllib = None


def load_toml(path: str = "archon.toml") -> dict:
    if tomllib is None or not os.path.isfile(path):
        return {}
    try:
        with open(path, "rb") as f:
            return tomllib.load(f)
    except Exception:
        return {}
