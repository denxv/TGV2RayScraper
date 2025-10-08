from argparse import ArgumentTypeError
from base64 import b64decode, b64encode, urlsafe_b64decode
from datetime import datetime
from pathlib import Path
from re import fullmatch, search, split

from core.logger import logger
from core.typing import (
    AbsPath,
    ArgsNamespace,
    AttrName,
    B64String,
    CLIFlag,
    CLIFlags,
    CLIParams,
    ConfigField,
    ConfigFields,
    FilePath,
    FilePaths,
    IntRangeValue,
    IntStr,
    MaxValue,
    MinValue,
    NormalizedParamsStr,
    ParamsStr,
    RegexPattern,
    RegexTarget,
)


def abs_path(path: FilePath) -> AbsPath:
    return str((Path(__file__).parent / path).resolve())


def b64decode_safe(string: B64String) -> B64String:
    if not isinstance(string, str) or not (string := string.strip()):
        return ""
    string = f"{string}{'=' * (-len(string) % 4)}"
    for b64_decode in (urlsafe_b64decode, b64decode):
        try:
            return b64_decode(string).decode('utf-8', errors='replace')
        except Exception:
            continue
    return ""


def b64encode_safe(string: B64String) -> B64String:
    return b64encode(string.encode('utf-8')).decode('ascii')


def collect_args(args: ArgsNamespace, flags: CLIFlags) -> CLIParams:
    params = []
    for flag in flags:
        value = getattr(args, flag_to_name(flag), None)
        if value is not None:
            params.extend([flag] if not value else [flag, value])
    return params


def flag_to_name(flag: CLIFlag) -> AttrName:
    return flag.lstrip('-').replace('-', '_')


def int_in_range(
    value: IntStr,
    min_value: MinValue = 1,
    max_value: MaxValue = 100,
    as_str: bool = False,
) -> IntRangeValue:
    ivalue = int(value)
    if ivalue < min_value or ivalue > max_value:
        raise ArgumentTypeError(f"Expected {min_value} to {max_value}, got {ivalue}")
    return str(ivalue) if as_str else ivalue


def make_backup(files: FilePaths) -> None:
    for file in files:
        src = Path(file).resolve()
        if not src.exists():
            continue
        backup_name = f"{src.stem}-backup-{datetime.now():%Y%m%d-%H%M%s}{src.suffix}"
        src.rename(src.parent / backup_name)
        logger.info(f"File '{src.name}' backed up as '{backup_name}'.")


def normalize_valid_fields(params_str: ParamsStr) -> NormalizedParamsStr:
    return ",".join(parse_valid_fields(params_str)) if params_str.strip() else ""


def parse_valid_fields(params_str: ParamsStr) -> ConfigFields:
    if not isinstance(params_str, str):
        raise ArgumentTypeError(f"Expected string, got {type(params_str).__name__!r}")

    seen_fields = set()

    def check_field(field: ConfigField) -> ConfigField:
        if not fullmatch(r"\w+(?:\.\w+)*", field):
            raise ArgumentTypeError(f"Invalid field format: {field!r}")
        if field in seen_fields:
            raise ArgumentTypeError(f"Duplicate field detected: {field!r}")
        seen_fields.add(field)
        return field

    valid_fields = [
        check_field(field)
        for field in split(r"[ ,]+", params_str.strip())
    ]

    if not valid_fields:
        raise ArgumentTypeError("No fields provided")

    return valid_fields


def re_fullmatch(pattern: RegexPattern, string: RegexTarget) -> bool:
    if not isinstance(string, str):
        string = str(string)
    return bool(fullmatch(pattern, string))


def re_search(pattern: RegexPattern, string: RegexTarget) -> bool:
    if not isinstance(string, str):
        string = str(string)
    return bool(search(pattern, string))


def validate_file_path(path: FilePath, must_be_file: bool = True) -> str:
    filepath = Path(path).resolve()

    if not filepath.parent.exists():
        raise ArgumentTypeError(f"Parent directory does not exist: '{filepath.parent}'.")

    if filepath.exists() and filepath.is_dir():
        raise ArgumentTypeError(f"'{filepath}' is a directory, expected a file.")

    if must_be_file and not filepath.is_file():
        raise ArgumentTypeError(f"The file does not exist: '{filepath}'.")

    return str(filepath)
