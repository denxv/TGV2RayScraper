from argparse import (
    ArgumentTypeError,
    Namespace,
)
from datetime import (
    datetime,
)
from pathlib import (
    Path,
)
from unittest.mock import (
    Mock,
)

import pytest

from core.utils import (
    abs_path,
    b64decode_safe,
    b64encode_safe,
    collect_args,
    convert_number_in_range,
    flag_to_name,
    make_backup,
    name_to_flag,
    normalize_scalar,
    normalize_valid_fields,
    parse_valid_fields,
    re_fullmatch,
    re_search,
    rel_path,
    repeat_char_line,
    validate_file_path,
)
from tests.unit.core.constants.common import (
    DEFAULT_PATH_PROJECT,
    FORMAT_BACKUP_DATE,
    TEMPLATE_ERROR_EXPECTED_FILE,
    TEMPLATE_ERROR_FILE_NOT_EXIST,
    TEMPLATE_ERROR_PARENT_DIRECTORY_NOT_EXIST,
    TEMPLATE_FORMAT_FILE_BACKUP_NAME,
    TEMPLATE_MSG_FILE_BACKUP_COMPLETED,
)
from tests.unit.core.constants.test_cases.utils import (
    ABS_PATH_ABSOLUTE_ARGS,
    ABS_PATH_ABSOLUTE_CASES,
    ABS_PATH_INVALID_TYPE_ARGS,
    ABS_PATH_INVALID_TYPE_CASES,
    ABS_PATH_RELATIVE_ARGS,
    ABS_PATH_RELATIVE_CASES,
    B64DECODE_SAFE_INVALID_INPUTS_ARGS,
    B64DECODE_SAFE_INVALID_INPUTS_CASES,
    B64DECODE_SAFE_VALID_AND_INVALID_ARGS,
    B64DECODE_SAFE_VALID_AND_INVALID_CASES,
    B64ENCODE_SAFE_INVALID_TYPE_ARGS,
    B64ENCODE_SAFE_INVALID_TYPE_CASES,
    B64ENCODE_SAFE_VALID_ARGS,
    B64ENCODE_SAFE_VALID_CASES,
    COLLECT_ARGS_COMBINED_ARGS,
    COLLECT_ARGS_COMBINED_CASES,
    CONVERT_NUMBER_IN_RANGE_INVALID_VALUE_ARGS,
    CONVERT_NUMBER_IN_RANGE_INVALID_VALUE_CASES,
    CONVERT_NUMBER_IN_RANGE_OUT_OF_BOUNDS_ARGS,
    CONVERT_NUMBER_IN_RANGE_OUT_OF_BOUNDS_CASES,
    CONVERT_NUMBER_IN_RANGE_VALID_ARGS,
    CONVERT_NUMBER_IN_RANGE_VALID_CASES,
    FLAG_NAME_ROUNDTRIP_ARGS,
    FLAG_NAME_ROUNDTRIP_CASES,
    NORMALIZE_SCALAR_ARGS,
    NORMALIZE_SCALAR_CASES,
    NORMALIZE_VALID_FIELDS_VALID_ARGS,
    NORMALIZE_VALID_FIELDS_VALID_CASES,
    PARSE_VALID_FIELDS_INVALID_ARGS,
    PARSE_VALID_FIELDS_INVALID_CASES,
    RE_FULLMATCH_AND_SEARCH_EXTENDED_ARGS,
    RE_FULLMATCH_AND_SEARCH_EXTENDED_CASES,
    REL_PATH_ARGS,
    REL_PATH_CASES,
    REPEAT_CHAR_LINE_ARGS,
    REPEAT_CHAR_LINE_CASES,
    VALIDATE_FILE_PATH_SUCCESS_ARGS,
    VALIDATE_FILE_PATH_SUCCESS_CASES,
)


def _validate_file_path_raises(
    path: Path,
    expected_msg_template: str,
    *,
    must_be_file: bool,
    is_parent: bool = False,
) -> None:
    with pytest.raises(ArgumentTypeError) as exc_info:
        validate_file_path(
            path=path,
            must_be_file=must_be_file,
        )

    if is_parent:
        expected_msg = expected_msg_template.format(
            parent=path.parent.resolve(),
        )
    else:
        expected_msg = expected_msg_template.format(
            filepath=path.resolve(),
        )

    assert str(exc_info.value) == expected_msg


@pytest.mark.parametrize(
    ABS_PATH_ABSOLUTE_ARGS,
    ABS_PATH_ABSOLUTE_CASES,
)
def test_abs_path_absolute(
    mock_module_files: Path,
    absolute_path: str | Path,
) -> None:
    result = abs_path(
        path=absolute_path,
    )

    assert isinstance(result, str)
    assert result == str(absolute_path)


@pytest.mark.parametrize(
    ABS_PATH_INVALID_TYPE_ARGS,
    ABS_PATH_INVALID_TYPE_CASES,
)
def test_abs_path_invalid_type(
    invalid_input: object,
) -> None:
    with pytest.raises(TypeError):
        abs_path(
            path=invalid_input,
        )


@pytest.mark.parametrize(
    ABS_PATH_RELATIVE_ARGS,
    ABS_PATH_RELATIVE_CASES,
)
def test_abs_path_relative(
    mock_module_files: Path,
    input_path: str,
) -> None:
    tmp_path = mock_module_files

    expected = str(
        (tmp_path / input_path).resolve(),
    )

    result = abs_path(
        path=input_path,
    )

    assert isinstance(result, str)
    assert result == expected


@pytest.mark.parametrize(
    B64DECODE_SAFE_INVALID_INPUTS_ARGS,
    B64DECODE_SAFE_INVALID_INPUTS_CASES,
)
def test_b64decode_safe_invalid_inputs(
    invalid_input: object,
) -> None:
    result = b64decode_safe(
        string=invalid_input,
    )

    assert result == ""


@pytest.mark.parametrize(
    B64DECODE_SAFE_VALID_AND_INVALID_ARGS,
    B64DECODE_SAFE_VALID_AND_INVALID_CASES,
)
def test_b64decode_safe_valid_and_invalid(
    input_str: str,
    expected_output: str,
) -> None:
    result = b64decode_safe(
        string=input_str,
    )

    assert isinstance(result, str)
    assert result == expected_output


@pytest.mark.parametrize(
    B64ENCODE_SAFE_INVALID_TYPE_ARGS,
    B64ENCODE_SAFE_INVALID_TYPE_CASES,
)
def test_b64encode_safe_invalid_type(
    invalid_input: object,
) -> None:
    with pytest.raises((
        AttributeError,
        TypeError,
    )):
        b64encode_safe(
            string=invalid_input,
        )


@pytest.mark.parametrize(
    B64ENCODE_SAFE_VALID_ARGS,
    B64ENCODE_SAFE_VALID_CASES,
)
def test_b64encode_safe_valid(
    input_str: str,
    expected_output: str,
) -> None:
    result = b64encode_safe(
        string=input_str,
    )

    assert isinstance(result, str)
    assert result == expected_output


@pytest.mark.parametrize(
    COLLECT_ARGS_COMBINED_ARGS,
    COLLECT_ARGS_COMBINED_CASES,
)
def test_collect_args_combined(
    args_namespace: Namespace,
    flags: list[str],
    expected: list[object],
) -> None:
    result = collect_args(
        args=args_namespace,
        flags=flags,
    )

    assert isinstance(result, list)
    assert result == expected


@pytest.mark.parametrize(
    CONVERT_NUMBER_IN_RANGE_INVALID_VALUE_ARGS,
    CONVERT_NUMBER_IN_RANGE_INVALID_VALUE_CASES,
)
def test_convert_number_in_range_invalid_value(
    value: str | None,
) -> None:
    with pytest.raises(ArgumentTypeError):
        convert_number_in_range(
            value=value,
        )


@pytest.mark.parametrize(
    CONVERT_NUMBER_IN_RANGE_OUT_OF_BOUNDS_ARGS,
    CONVERT_NUMBER_IN_RANGE_OUT_OF_BOUNDS_CASES,
)
def test_convert_number_in_range_out_of_bounds(
    value: str,
    min_value: int,
    max_value: int,
) -> None:
    with pytest.raises(ArgumentTypeError):
        convert_number_in_range(
            value=value,
            min_value=min_value,
            max_value=max_value,
        )


@pytest.mark.parametrize(
    CONVERT_NUMBER_IN_RANGE_VALID_ARGS,
    CONVERT_NUMBER_IN_RANGE_VALID_CASES,
)
def test_convert_number_in_range_valid(
    value: str,
    min_value: int,
    max_value: int,
    *,
    as_int: bool,
    as_str: bool,
    expected: float | str,
) -> None:
    result = convert_number_in_range(
        value=value,
        min_value=min_value,
        max_value=max_value,
        as_int=as_int,
        as_str=as_str,
    )

    if as_str:
        assert isinstance(result, str)
    else:
        assert isinstance(
            result,
            int if as_int else float,
        )

    assert result == expected


@pytest.mark.parametrize(
    FLAG_NAME_ROUNDTRIP_ARGS,
    FLAG_NAME_ROUNDTRIP_CASES,
)
def test_flag_name_roundtrip(
    flag: str,
    name: str,
) -> None:
    result_name = flag_to_name(
        flag=flag,
    )

    assert isinstance(result_name, str)
    assert result_name == name

    result_flag = name_to_flag(
        name=name,
    )

    assert isinstance(result_flag, str)
    assert result_flag.startswith("--")
    assert result_flag.lstrip("-").replace("-", "_") == name


def test_make_backup(
    mock_logger: Mock,
    frozen_datetime_local_tz: datetime,
    tmp_files: list[Path],
) -> None:
    make_backup(
        files=[
            str(file)
            for file in tmp_files
        ],
    )

    assert not tmp_files[0].exists()

    for file in tmp_files[1:]:
        backup_name = TEMPLATE_FORMAT_FILE_BACKUP_NAME.format(
            stem=file.stem,
            date=frozen_datetime_local_tz.strftime(
                FORMAT_BACKUP_DATE,
            ),
            suffix=file.suffix,
        )
        backup_path = file.parent / backup_name

        assert backup_path.exists()
        assert not file.exists()

        mock_logger.info.assert_any_call(
            msg=TEMPLATE_MSG_FILE_BACKUP_COMPLETED.format(
                src_name=file.name,
                backup_name=backup_name,
            ),
        )


@pytest.mark.parametrize(
    NORMALIZE_SCALAR_ARGS,
    NORMALIZE_SCALAR_CASES,
)
def test_normalize_scalar(
    value: object,
    *,
    as_str: bool,
    expected: int | str | None,
) -> None:
    result = normalize_scalar(
        value=value,
        as_str=as_str,
    )

    assert result == expected


@pytest.mark.parametrize(
    NORMALIZE_VALID_FIELDS_VALID_ARGS,
    NORMALIZE_VALID_FIELDS_VALID_CASES,
)
def test_normalize_valid_fields_valid(
    input_str: str,
    expected: str,
) -> None:
    result = normalize_valid_fields(
        params_str=input_str,
    )

    assert result == expected


@pytest.mark.parametrize(
    PARSE_VALID_FIELDS_INVALID_ARGS,
    PARSE_VALID_FIELDS_INVALID_CASES,
)
def test_parse_valid_fields_invalid(
    invalid_input: object,
) -> None:
    with pytest.raises(ArgumentTypeError):
        parse_valid_fields(
            params_str=invalid_input,
        )


@pytest.mark.parametrize(
    RE_FULLMATCH_AND_SEARCH_EXTENDED_ARGS,
    RE_FULLMATCH_AND_SEARCH_EXTENDED_CASES,
)
def test_re_fullmatch_and_search_extended(
    pattern: str,
    string: float | None | str,
    *,
    expected_fullmatch: bool,
    expected_search: bool,
) -> None:
    result_fullmatch = re_fullmatch(
        pattern=pattern,
        string=string,
    )

    result_search = re_search(
        pattern=pattern,
        string=string,
    )

    assert result_fullmatch is expected_fullmatch
    assert result_search is expected_search


@pytest.mark.parametrize(
    REL_PATH_ARGS,
    REL_PATH_CASES,
)
def test_rel_path(
    input_path: str,
) -> None:
    root = DEFAULT_PATH_PROJECT

    if not Path(input_path).is_absolute():
        test_path = (root / input_path).resolve()
    else:
        test_path = Path(input_path).resolve()

    result = rel_path(
        path=test_path,
        root=root,
    )

    if test_path.is_relative_to(root):
        expected = str(test_path.relative_to(root.resolve()))
    else:
        expected = str(test_path)

    assert isinstance(result, str)
    assert result == expected


@pytest.mark.parametrize(
    REPEAT_CHAR_LINE_ARGS,
    REPEAT_CHAR_LINE_CASES,
)
def test_repeat_char_line(
    char: str,
    length: int,
    expected: str,
) -> None:
    result = repeat_char_line(
        char=char,
        length=length,
    )

    assert isinstance(result, str)
    assert result == expected
    assert len(result) == length
    assert all(
        c == char
        for c in result
    )


def test_validate_file_path_is_directory(tmp_path: Path) -> None:
    _validate_file_path_raises(
        path=tmp_path,
        expected_msg_template=TEMPLATE_ERROR_EXPECTED_FILE,
        must_be_file=True,
        is_parent=False,
    )


def test_validate_file_path_missing_file(tmp_path: Path) -> None:
    _validate_file_path_raises(
        path=tmp_path / "missing.txt",
        expected_msg_template=TEMPLATE_ERROR_FILE_NOT_EXIST,
        must_be_file=True,
        is_parent=False,
    )


def test_validate_file_path_parent_missing(tmp_path: Path) -> None:
    _validate_file_path_raises(
        path=tmp_path / "missing_dir" / "file.txt",
        expected_msg_template=TEMPLATE_ERROR_PARENT_DIRECTORY_NOT_EXIST,
        must_be_file=True,
        is_parent=True,
    )


@pytest.mark.parametrize(
    VALIDATE_FILE_PATH_SUCCESS_ARGS,
    VALIDATE_FILE_PATH_SUCCESS_CASES,
)
def test_validate_file_path_success(
    tmp_path: Path,
    filename: str,
    *,
    must_be_file: bool,
) -> None:
    file_path = tmp_path / filename

    if (
        must_be_file
        and filename == "file.txt"
    ):
        file_path.write_text("content")

    result = validate_file_path(
        path=file_path,
        must_be_file=must_be_file,
    )

    assert result == str(
        file_path.resolve(),
    )
    assert Path(result).resolve() == file_path.resolve()
