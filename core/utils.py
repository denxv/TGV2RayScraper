from argparse import (
    ArgumentTypeError,
)
from base64 import (
    b64encode,
    urlsafe_b64decode,
)
from datetime import (
    datetime,
)
from json import (
    dumps,
)
from pathlib import (
    Path,
)
from re import (
    fullmatch,
    search,
)

from core.constants.common import (
    BASE64_BLOCK_SIZE,
    DEFAULT_LOG_LINE_LENGTH,
    DEFAULT_PATH_PROJECT,
    DEFAULT_VALUE_MAX,
    DEFAULT_VALUE_MIN,
)
from core.constants.formats import (
    FORMAT_BACKUP_DATE,
)
from core.constants.messages import (
    MESSAGE_ERROR_NO_FIELDS_PROVIDED,
)
from core.constants.patterns import (
    PATTERN_CONFIG_FIELD,
    PATTERN_PARAM_SEPARATOR,
)
from core.constants.templates import (
    TEMPLATE_ERROR_DETECTED_DUPLICATE_FIELD,
    TEMPLATE_ERROR_EXPECTED_FILE,
    TEMPLATE_ERROR_EXPECTED_STRING,
    TEMPLATE_ERROR_FILE_NOT_EXIST,
    TEMPLATE_ERROR_INVALID_FIELD,
    TEMPLATE_ERROR_INVALID_NUMBER,
    TEMPLATE_ERROR_NUMBER_OUT_OF_RANGE,
    TEMPLATE_ERROR_PARENT_DIRECTORY_NOT_EXIST,
    TEMPLATE_FORMAT_FILE_BACKUP_NAME,
    TEMPLATE_FORMAT_STRING_BASE64_PADDING,
    TEMPLATE_MSG_FILE_BACKUP_COMPLETED,
)
from core.logger import (
    logger,
)
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

__all__ = [
    "abs_path",
    "b64decode_safe",
    "b64encode_safe",
    "collect_args",
    "convert_number_in_range",
    "flag_to_name",
    "make_backup",
    "name_to_flag",
    "normalize_scalar",
    "normalize_valid_fields",
    "parse_valid_fields",
    "re_fullmatch",
    "re_search",
    "repeat_char_line",
    "validate_file_path",
]


def abs_path(
    path: FilePath,
) -> AbsPath:
    return str(
        (Path(__file__).parent / path).resolve(),
    )


def b64decode_safe(
    string: B64String,
) -> B64String:
    if (
        not (
            isinstance(string, str)
            and (string := string.strip())
        )
    ):
        return ""

    string = TEMPLATE_FORMAT_STRING_BASE64_PADDING.format(
        string=string,
        padding="=" * (-len(string) % BASE64_BLOCK_SIZE),
    )

    try:
        b64_decoded_bytes = urlsafe_b64decode(
            s=string,
        )
    except Exception:
        return ""
    else:
        return b64_decoded_bytes.decode(
            encoding="utf-8",
            errors="replace",
        )


def b64encode_safe(
    string: B64String,
) -> B64String:
    encoded_bytes = string.encode(
        encoding="utf-8",
    )
    b64_encoded_bytes = b64encode(
        s=encoded_bytes,
    )

    return b64_encoded_bytes.decode(
        encoding="ascii",
    )


def collect_args(
    args: ArgsNamespace,
    flags: CLIFlags,
) -> CLIParams:
    params = []

    for flag in flags:
        attr_name = flag_to_name(
            flag=flag,
        )
        value = getattr(
            args,
            attr_name,
            None,
        )

        if value is None:
            continue

        cli_flag = name_to_flag(
            name=attr_name,
        )

        if (
            isinstance(value, bool)
            or (isinstance(value, str) and not value)
        ):
            params.append(cli_flag)
        else:
            params.extend([
                cli_flag,
                value,
            ])

    return params


def convert_number_in_range(
    value: FloatStr,
    min_value: MinValue = DEFAULT_VALUE_MIN,
    max_value: MaxValue = DEFAULT_VALUE_MAX,
    *,
    as_int: bool = True,
    as_str: bool = False,
) -> NumberValue:
    try:
        _value = int(value) if as_int else float(value)
    except (
        TypeError,
        ValueError,
    ):
        _message = TEMPLATE_ERROR_INVALID_NUMBER.format(
            value=value,
        )
        raise ArgumentTypeError(_message) from None

    if (
        _value < min_value
        or _value > max_value
    ):
        raise ArgumentTypeError(
            TEMPLATE_ERROR_NUMBER_OUT_OF_RANGE.format(
                min_value=min_value,
                max_value=max_value,
                value=_value,
            ),
        )

    return str(_value) if as_str else _value


def flag_to_name(
    flag: CLIFlag,
) -> AttrName:
    cleaned_flag = flag.lstrip("-")
    return cleaned_flag.replace("-", "_")


def make_backup(
    files: FilePaths,
) -> None:
    now = datetime.now().astimezone().strftime(
        FORMAT_BACKUP_DATE,
    )

    for file in files:
        src = Path(file).resolve()

        if not src.exists():
            continue

        backup_name = TEMPLATE_FORMAT_FILE_BACKUP_NAME.format(
            stem=src.stem,
            date=now,
            suffix=src.suffix,
        )
        src.rename(
            target=src.parent / backup_name,
        )

        logger.info(
            msg=TEMPLATE_MSG_FILE_BACKUP_COMPLETED.format(
                src_name=src.name,
                backup_name=backup_name,
            ),
        )


def name_to_flag(
    name: AttrName,
) -> CLIFlag:
    return "--" + name.replace("_", "-")


def normalize_scalar(
    value: ComplexValue,
    *,
    as_str: bool = False,
) -> ScalarValue:
    if value is None:
        return None

    if isinstance(
        value,
        (
            dict,
            list,
            tuple,
        ),
    ):
        return dumps(
            obj=value,
            sort_keys=True,
            separators=(",", ":"),
        )

    return str(value) if as_str else value


def normalize_valid_fields(
    params_str: ParamsStr,
) -> NormalizedParamsStr:
    if not params_str.strip():
        return ""

    return ",".join(
        parse_valid_fields(params_str),
    )


def parse_valid_fields(
    params_str: ParamsStr,
) -> ConfigFields:
    if not isinstance(params_str, str):
        raise ArgumentTypeError(
            TEMPLATE_ERROR_EXPECTED_STRING.format(
                type_name=type(params_str).__name__,
            ),
        )

    seen_fields = set()

    def check_field(
        field: ConfigField,
    ) -> ConfigField:
        if not PATTERN_CONFIG_FIELD.fullmatch(
            string=field,
        ):
            raise ArgumentTypeError(
                TEMPLATE_ERROR_INVALID_FIELD.format(
                    field=field,
                ),
            )

        if field in seen_fields:
            raise ArgumentTypeError(
                TEMPLATE_ERROR_DETECTED_DUPLICATE_FIELD.format(
                    field=field,
                ),
            )

        seen_fields.add(field)

        return field

    valid_fields = [
        check_field(
            field=field,
        )
        for field in PATTERN_PARAM_SEPARATOR.split(
            string=params_str.strip(),
        )
    ]

    if not valid_fields:  # pragma: no cover
        raise ArgumentTypeError(
            MESSAGE_ERROR_NO_FIELDS_PROVIDED,
        )

    return valid_fields


def re_fullmatch(
    pattern: RegexPattern,
    string: RegexTarget,
) -> bool:
    if not isinstance(string, str):
        string = str(string)

    return bool(
        fullmatch(
            pattern=pattern,
            string=string,
        ),
    )


def re_search(
    pattern: RegexPattern,
    string: RegexTarget,
) -> bool:
    if not isinstance(string, str):
        string = str(string)

    return bool(
        search(
            pattern=pattern,
            string=string,
        ),
    )


def rel_path(
    path: FilePath,
    root: FilePath = DEFAULT_PATH_PROJECT,
) -> str:
    path, root = Path(path).resolve(), Path(root).resolve()
    return (
        str(path.relative_to(root))
        if path.is_relative_to(root) else str(path)
    )


def repeat_char_line(
    char: str = "-",
    length: int = DEFAULT_LOG_LINE_LENGTH,
) -> str:
    return char * length


def validate_file_path(
    path: FilePath,
    *,
    must_be_file: bool = True,
) -> str:
    filepath = Path(path).resolve()

    if not filepath.parent.exists():
        raise ArgumentTypeError(
            TEMPLATE_ERROR_PARENT_DIRECTORY_NOT_EXIST.format(
                parent=filepath.parent,
            ),
        )

    if (
        filepath.exists()
        and filepath.is_dir()
    ):
        raise ArgumentTypeError(
            TEMPLATE_ERROR_EXPECTED_FILE.format(
                filepath=filepath,
            ),
        )

    if (
        must_be_file
        and not filepath.is_file()
    ):
        raise ArgumentTypeError(
            TEMPLATE_ERROR_FILE_NOT_EXIST.format(
                filepath=filepath,
            ),
        )

    return str(filepath)
