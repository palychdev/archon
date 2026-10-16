from dataclasses import dataclass


@dataclass
class ScanConfig:
    max_depth: int = 5
    max_size_mb: int = 512
    scan_archives: bool = True
    timeout_sec: int = 600
    exclude: tuple[str, ...] = ()
