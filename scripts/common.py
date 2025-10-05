from pathlib import Path


def abs_path(path: str | Path) -> str:
    return str((Path(__file__).parent / path).resolve())

