from argparse import ArgumentTypeError, Namespace
from base64 import b64decode, b64encode, urlsafe_b64decode
from datetime import datetime
from pathlib import Path
from re import fullmatch, search, split

from core.logger import logger


def abs_path(path: str | Path) -> str:
    return str((Path(__file__).parent / path).resolve())


def b64decode_safe(string: str) -> str:
    if not isinstance(string, str) or not (string := string.strip()):
        return ""
    string = f"{string}{'=' * (-len(string) % 4)}"
    for b64_decode in (urlsafe_b64decode, b64decode):
        try:
            return b64_decode(string).decode('utf-8', errors='replace')
        except Exception:
            continue
    return ""


def b64encode_safe(string: str) -> str:
    return b64encode(string.encode('utf-8')).decode('ascii')


def collect_args(args: Namespace, flags: list[str]) -> list[str]:
    params = []
    for flag in flags:
        value = getattr(args, flag_to_name(flag), None)
        if value is not None:
            params.extend([flag] if not value else [flag, value])
    return params


def flag_to_name(flag: str) -> str:
    return flag.lstrip('-').replace('-', '_')


def int_in_range(
    value: str,
    min_value: int = 1,
    max_value: int = 100,
    as_str: bool = False,
) -> int | str:
    ivalue = int(value)
    if ivalue < min_value or ivalue > max_value:
        raise ArgumentTypeError(f"Expected {min_value} to {max_value}, got {ivalue}")
    return str(ivalue) if as_str else ivalue


def make_backup(files: list[str | Path]) -> None:
    for file in files:
        src = Path(file).resolve()
        if not src.exists():
            continue
        backup_name = f"{src.stem}-backup-{datetime.now():%Y%m%d-%H%M%s}{src.suffix}"
        src.rename(src.parent / backup_name)
        logger.info(f"File '{src.name}' backed up as '{backup_name}'.")


def normalize_valid_params(params: str) -> str:
    return ",".join(parse_valid_params(params)) if params.strip() else ""


def parse_valid_params(params: str) -> list[str]:
    if not isinstance(params, str):
        raise ArgumentTypeError(f"Expected string, got {type(params).__name__!r}")

    seen = set()

    def check_param(param: str) -> str:
        if not fullmatch(r"\w+(?:\.\w+)*", param):
            raise ArgumentTypeError(f"Invalid parameter: {param!r}")
        if param in seen:
            raise ArgumentTypeError(f"Duplicate parameter: {param!r}")
        seen.add(param)
        return param

    valid_params = [
        check_param(param)
        for param in split(r"[ ,]+", params.strip())
    ]

    if not valid_params:
        raise ArgumentTypeError("No parameters provided")

    return valid_params


def re_fullmatch(pattern: str, string: str) -> bool:
    if not isinstance(string, str):
        string = str(string)
    return bool(fullmatch(pattern, string))


def re_search(pattern: str, string: str) -> bool:
    if not isinstance(string, str):
        string = str(string)
    return bool(search(pattern, string))


def validate_file_path(path: str | Path, must_be_file: bool = True) -> str:
    filepath = Path(path).resolve()

    if not filepath.parent.exists():
        raise ArgumentTypeError(f"Parent directory does not exist: '{filepath.parent}'.")

    if filepath.exists() and filepath.is_dir():
        raise ArgumentTypeError(f"'{filepath}' is a directory, expected a file.")

    if must_be_file and not filepath.is_file():
        raise ArgumentTypeError(f"The file does not exist: '{filepath}'.")

    return str(filepath)
