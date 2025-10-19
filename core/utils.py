from argparse import ArgumentTypeError
from base64 import b64decode, b64encode, urlsafe_b64decode
from datetime import datetime
from json import dumps
from pathlib import Path
from re import fullmatch, search

from core.constants import (
    BASE64_BLOCK_SIZE,
    DEFAULT_LOG_LINE_LENGTH,
    DEFAULT_MAX_VALUE,
    DEFAULT_MIN_VALUE,
    FORMAT_BACKUP_DATE,
    MESSAGE_NO_FIELDS_PROVIDED,
    PATTERN_CONFIG_FIELD,
    PATTERN_PARAM_SEPARATOR,
    TEMPLATE_BACKUP_FILENAME,
    TEMPLATE_MSG_DUPLICATE_FIELD,
    TEMPLATE_MSG_EXPECTED_STRING,
    TEMPLATE_MSG_FILE_BACKED_UP,
    TEMPLATE_MSG_FILE_DOES_NOT_EXIST,
    TEMPLATE_MSG_INVALID_FIELD_FORMAT,
    TEMPLATE_MSG_INVALID_NUMBER,
    TEMPLATE_MSG_IS_DIRECTORY,
    TEMPLATE_MSG_NUMBER_OUT_OF_RANGE,
    TEMPLATE_MSG_PARENT_DIR_MISSING,
)
from core.logger import logger
from core.typing import (
    AbsPath,
    ArgsNamespace,
    AttrName,
    B64String,
    CLIFlag,
    CLIFlags,
    CLIParams,
    ComplexValue,
    ConfigField,
    ConfigFields,
    FilePath,
    FilePaths,
    FloatStr,
    MaxValue,
    MinValue,
    NormalizedParamsStr,
    NumberValue,
    ParamsStr,
    RegexPattern,
    RegexTarget,
    ScalarValue,
)


def abs_path(path: FilePath) -> AbsPath:
    return str((Path(__file__).parent / path).resolve())


def b64decode_safe(string: B64String) -> B64String:
    if not isinstance(string, str) or not (string := string.strip()):
        return ""

    string = f"{string}{"=" * (-len(string) % BASE64_BLOCK_SIZE)}"
    for b64_decode in (urlsafe_b64decode, b64decode):
        try:
            return b64_decode(string).decode("utf-8", errors="replace")
        except Exception:  # noqa: S112
            continue

    return ""


def b64encode_safe(string: B64String) -> B64String:
    return b64encode(string.encode("utf-8")).decode("ascii")


def collect_args(args: ArgsNamespace, flags: CLIFlags) -> CLIParams:
    params = []
    for flag in flags:
        value = getattr(args, flag_to_name(flag), None)
        if value is not None:
            params.extend([flag] if not value else [flag, value])

    return params


def convert_number_in_range(
    value: FloatStr,
    min_value: MinValue = DEFAULT_MIN_VALUE,
    max_value: MaxValue = DEFAULT_MAX_VALUE,
    *,
    as_int: bool = True,
    as_str: bool = False,
) -> NumberValue:
    try:
        _value = int(value) if as_int else float(value)
    except ValueError:
        _message = TEMPLATE_MSG_INVALID_NUMBER.format(value=value)
        raise ArgumentTypeError(_message) from None

    if not min_value <= _value <= max_value:
        raise ArgumentTypeError(TEMPLATE_MSG_NUMBER_OUT_OF_RANGE.format(
            min_value=min_value,
            max_value=max_value,
            value=_value,
        ))

    return str(_value) if as_str else _value


def flag_to_name(flag: CLIFlag) -> AttrName:
    return flag.lstrip("-").replace("-", "_")


def make_backup(files: FilePaths) -> None:
    now = datetime.now().astimezone().strftime(FORMAT_BACKUP_DATE)
    for file in files:
        src = Path(file).resolve()
        if not src.exists():
            continue

        backup_name = TEMPLATE_BACKUP_FILENAME.format(
            stem=src.stem,
            date=now,
            suffix=src.suffix,
        )

        src.rename(src.parent / backup_name)
        logger.info(TEMPLATE_MSG_FILE_BACKED_UP.format(
            src_name=src.name,
            backup_name=backup_name,
        ))


def normalize_scalar(
    value: ComplexValue,
    *,
    as_str: bool = False,
) -> ScalarValue:
    if value is None:
        return None

    if isinstance(value, (dict, list, tuple)):
        return dumps(value, sort_keys=True, separators=(",", ":"))

    return str(value) if as_str else value


def normalize_valid_fields(params_str: ParamsStr) -> NormalizedParamsStr:
    if not params_str.strip():
        return ""

    return ",".join(parse_valid_fields(params_str))


def parse_valid_fields(params_str: ParamsStr) -> ConfigFields:
    if not isinstance(params_str, str):
        raise ArgumentTypeError(TEMPLATE_MSG_EXPECTED_STRING.format(
            type_name=type(params_str).__name__,
        ))

    seen_fields = set()

    def check_field(field: ConfigField) -> ConfigField:
        if not PATTERN_CONFIG_FIELD.fullmatch(field):
            raise ArgumentTypeError(
                TEMPLATE_MSG_INVALID_FIELD_FORMAT.format(field=field),
            )

        if field in seen_fields:
            raise ArgumentTypeError(
                TEMPLATE_MSG_DUPLICATE_FIELD.format(field=field),
            )

        seen_fields.add(field)
        return field

    valid_fields = [
        check_field(field)
        for field in PATTERN_PARAM_SEPARATOR.split(params_str.strip())
    ]

    if not valid_fields:
        raise ArgumentTypeError(MESSAGE_NO_FIELDS_PROVIDED)

    return valid_fields


def re_fullmatch(pattern: RegexPattern, string: RegexTarget) -> bool:
    if not isinstance(string, str):
        string = str(string)

    return bool(fullmatch(pattern, string))


def re_search(pattern: RegexPattern, string: RegexTarget) -> bool:
    if not isinstance(string, str):
        string = str(string)

    return bool(search(pattern, string))


def repeat_char_line(
    char: str = "-",
    length: int = DEFAULT_LOG_LINE_LENGTH,
) -> str:
    return char * length


def validate_file_path(path: FilePath, *, must_be_file: bool = True) -> str:
    filepath = Path(path).resolve()

    if not filepath.parent.exists():
        raise ArgumentTypeError(TEMPLATE_MSG_PARENT_DIR_MISSING.format(
            parent=filepath.parent,
        ))

    if filepath.exists() and filepath.is_dir():
        raise ArgumentTypeError(
            TEMPLATE_MSG_IS_DIRECTORY.format(filepath=filepath),
        )

    if must_be_file and not filepath.is_file():
        raise ArgumentTypeError(
            TEMPLATE_MSG_FILE_DOES_NOT_EXIST.format(filepath=filepath),
        )

    return str(filepath)
