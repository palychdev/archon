import os
import sys


def list_run_keys() -> list[str]:
    if sys.platform != "win32":
        return []
    import winreg

    found: list[str] = []
    roots = [
        (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run"),
        (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run"),
    ]
    for hive, sub in roots:
        try:
            k = winreg.OpenKey(hive, sub)
        except OSError:
            continue
        i = 0
        while True:
            try:
                name, val, _ = winreg.EnumValue(k, i)
                found.append(f"{name} -> {val}")
                i += 1
            except OSError:
                break
    return found


def list_startup() -> list[str]:
    if sys.platform != "win32":
        return []
    base = os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup")
    if not os.path.isdir(base):
        return []
    return sorted(os.listdir(base))
