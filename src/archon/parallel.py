from concurrent.futures import ThreadPoolExecutor


def map_files(func, files: list[str], workers: int = 8) -> list:
    with ThreadPoolExecutor(max_workers=workers) as ex:
        return list(ex.map(func, files))
