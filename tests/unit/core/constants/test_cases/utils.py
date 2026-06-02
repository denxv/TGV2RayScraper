import pytest

from tests.unit.core.constants.examples.utils import (
    ABS_PATH_ABSOLUTE_EXAMPLES,
    ABS_PATH_INVALID_TYPE_EXAMPLES,
    ABS_PATH_RELATIVE_EXAMPLES,
    B64DECODE_SAFE_INVALID_INPUTS_EXAMPLES,
    B64DECODE_SAFE_VALID_AND_INVALID_EXAMPLES,
    B64ENCODE_SAFE_INVALID_TYPE_EXAMPLES,
    B64ENCODE_SAFE_VALID_EXAMPLES,
    BATCHED_EXAMPLES,
    COLLECT_ARGS_COMBINED_EXAMPLES,
    CONVERT_NUMBER_IN_RANGE_INVALID_VALUE_EXAMPLES,
    CONVERT_NUMBER_IN_RANGE_OUT_OF_BOUNDS_EXAMPLES,
    CONVERT_NUMBER_IN_RANGE_VALID_EXAMPLES,
    FLAG_NAME_ROUNDTRIP_EXAMPLES,
    GET_BATCHES_COUNT_EXAMPLES,
    NORMALIZE_CONDITION_INVALID_EXAMPLES,
    NORMALIZE_CONDITION_VALID_EXAMPLES,
    NORMALIZE_SCALAR_EXAMPLES,
    NORMALIZE_VALID_FIELDS_VALID_EXAMPLES,
    PARSE_VALID_FIELDS_INVALID_EXAMPLES,
    RE_FULLMATCH_AND_SEARCH_EXAMPLES,
    REL_PATH_EXAMPLES,
    VALIDATE_FILE_PATH_SUCCESS_EXAMPLES,
    VALIDATE_PROXY_URL_INVALID_EXAMPLES,
    VALIDATE_PROXY_URL_VALID_EXAMPLES,
)

__all__ = [
    "ABS_PATH_ABSOLUTE_ARGS",
    "ABS_PATH_ABSOLUTE_CASES",
    "ABS_PATH_INVALID_TYPE_ARGS",
    "ABS_PATH_INVALID_TYPE_CASES",
    "ABS_PATH_RELATIVE_ARGS",
    "ABS_PATH_RELATIVE_CASES",
    "B64DECODE_SAFE_INVALID_INPUTS_ARGS",
    "B64DECODE_SAFE_INVALID_INPUTS_CASES",
    "B64DECODE_SAFE_VALID_AND_INVALID_ARGS",
    "B64DECODE_SAFE_VALID_AND_INVALID_CASES",
    "B64ENCODE_SAFE_INVALID_TYPE_ARGS",
    "B64ENCODE_SAFE_INVALID_TYPE_CASES",
    "B64ENCODE_SAFE_VALID_ARGS",
    "B64ENCODE_SAFE_VALID_CASES",
    "BATCHED_ARGS",
    "BATCHED_CASES",
    "COLLECT_ARGS_COMBINED_ARGS",
    "COLLECT_ARGS_COMBINED_CASES",
    "CONVERT_NUMBER_IN_RANGE_INVALID_VALUE_ARGS",
    "CONVERT_NUMBER_IN_RANGE_INVALID_VALUE_CASES",
    "CONVERT_NUMBER_IN_RANGE_OUT_OF_BOUNDS_ARGS",
    "CONVERT_NUMBER_IN_RANGE_OUT_OF_BOUNDS_CASES",
    "CONVERT_NUMBER_IN_RANGE_VALID_ARGS",
    "CONVERT_NUMBER_IN_RANGE_VALID_CASES",
    "FLAG_NAME_ROUNDTRIP_ARGS",
    "FLAG_NAME_ROUNDTRIP_CASES",
    "GET_BATCHES_COUNT_ARGS",
    "GET_BATCHES_COUNT_CASES",
    "NORMALIZE_CONDITION_INVALID_ARGS",
    "NORMALIZE_CONDITION_INVALID_CASES",
    "NORMALIZE_CONDITION_VALID_ARGS",
    "NORMALIZE_CONDITION_VALID_CASES",
    "NORMALIZE_SCALAR_ARGS",
    "NORMALIZE_SCALAR_CASES",
    "NORMALIZE_VALID_FIELDS_VALID_ARGS",
    "NORMALIZE_VALID_FIELDS_VALID_CASES",
    "PARSE_VALID_FIELDS_INVALID_ARGS",
    "PARSE_VALID_FIELDS_INVALID_CASES",
    "REL_PATH_ARGS",
    "REL_PATH_CASES",
    "RE_FULLMATCH_AND_SEARCH_EXTENDED_ARGS",
    "RE_FULLMATCH_AND_SEARCH_EXTENDED_CASES",
    "VALIDATE_FILE_PATH_SUCCESS_ARGS",
    "VALIDATE_FILE_PATH_SUCCESS_CASES",
    "VALIDATE_PROXY_URL_INVALID_ARGS",
    "VALIDATE_PROXY_URL_INVALID_CASES",
    "VALIDATE_PROXY_URL_VALID_ARGS",
    "VALIDATE_PROXY_URL_VALID_CASES",
]

ABS_PATH_ABSOLUTE_ARGS: tuple[
    str,
    ...,
] = (
    "absolute_path",
)
ABS_PATH_ABSOLUTE_CASES: tuple[
    object,
    ...,
] = tuple(
    pytest.param(
        absolute_path,
        id=case_id,
    )
    for (
        absolute_path,
        case_id,
    ) in ABS_PATH_ABSOLUTE_EXAMPLES
)

ABS_PATH_INVALID_TYPE_ARGS: tuple[
    str,
    ...,
] = (
    "invalid_input",
)
ABS_PATH_INVALID_TYPE_CASES: tuple[
    object,
    ...,
] = tuple(
    pytest.param(
        invalid_input,
        id=case_id,
    )
    for (
        invalid_input,
        case_id,
    ) in ABS_PATH_INVALID_TYPE_EXAMPLES
)

ABS_PATH_RELATIVE_ARGS: tuple[
    str,
    ...,
] = (
    "input_path",
)
ABS_PATH_RELATIVE_CASES: tuple[
    object,
    ...,
] = tuple(
    pytest.param(
        input_path,
        id=case_id,
    )
    for (
        input_path,
        case_id,
    ) in ABS_PATH_RELATIVE_EXAMPLES
)

B64DECODE_SAFE_INVALID_INPUTS_ARGS: tuple[
    str,
    ...,
] = (
    "invalid_input",
)
B64DECODE_SAFE_INVALID_INPUTS_CASES: tuple[
    object,
    ...,
] = tuple(
    pytest.param(
        invalid_input,
        id=case_id,
    )
    for (
        invalid_input,
        case_id,
    ) in B64DECODE_SAFE_INVALID_INPUTS_EXAMPLES
)

B64DECODE_SAFE_VALID_AND_INVALID_ARGS: tuple[
    str,
    ...,
] = (
    "input_str",
    "expected_output",
)
B64DECODE_SAFE_VALID_AND_INVALID_CASES: tuple[
    object,
    ...,
] = tuple(
    pytest.param(
        input_str,
        expected_output,
        id=case_id,
    )
    for (
        input_str,
        expected_output,
        case_id,
    ) in B64DECODE_SAFE_VALID_AND_INVALID_EXAMPLES
)

B64ENCODE_SAFE_INVALID_TYPE_ARGS: tuple[
    str,
    ...,
] = (
    "invalid_input",
)
B64ENCODE_SAFE_INVALID_TYPE_CASES: tuple[
    object,
    ...,
] = tuple(
    pytest.param(
        invalid_input,
        id=case_id,
    )
    for (
        invalid_input,
        case_id,
    ) in B64ENCODE_SAFE_INVALID_TYPE_EXAMPLES
)

B64ENCODE_SAFE_VALID_ARGS: tuple[
    str,
    ...,
] = (
    "input_str",
    "expected_output",
)
B64ENCODE_SAFE_VALID_CASES: tuple[
    object,
    ...,
] = tuple(
    pytest.param(
        input_str,
        expected_output,
        id=case_id,
    )
    for (
        input_str,
        expected_output,
        case_id,
    ) in B64ENCODE_SAFE_VALID_EXAMPLES
)

BATCHED_ARGS: tuple[
    str,
    ...,
] = (
    "iterable",
    "size",
    "expected",
)
BATCHED_CASES: tuple[
    object,
    ...,
] = tuple(
    pytest.param(
        iterable,
        size,
        expected,
        id=case_id,
    )
    for (
        iterable,
        size,
        expected,
        case_id,
    ) in BATCHED_EXAMPLES
)

COLLECT_ARGS_COMBINED_ARGS: tuple[
    str,
    ...,
] = (
    "args_namespace",
    "flags",
    "expected",
)
COLLECT_ARGS_COMBINED_CASES: tuple[
    object,
    ...,
] = tuple(
    pytest.param(
        args_namespace,
        flags,
        expected,
        id=case_id,
    )
    for (
        args_namespace,
        flags,
        expected,
        case_id,
    ) in COLLECT_ARGS_COMBINED_EXAMPLES
)

CONVERT_NUMBER_IN_RANGE_INVALID_VALUE_ARGS: tuple[
    str,
    ...,
] = (
    "value",
)
CONVERT_NUMBER_IN_RANGE_INVALID_VALUE_CASES: tuple[
    object,
    ...,
] = tuple(
    pytest.param(
        value,
        id=case_id,
    )
    for (
        value,
        case_id,
    ) in CONVERT_NUMBER_IN_RANGE_INVALID_VALUE_EXAMPLES
)

CONVERT_NUMBER_IN_RANGE_OUT_OF_BOUNDS_ARGS: tuple[
    str,
    ...,
] = (
    "value",
    "min_value",
    "max_value",
)
CONVERT_NUMBER_IN_RANGE_OUT_OF_BOUNDS_CASES: tuple[
    object,
    ...,
] = tuple(
    pytest.param(
        value,
        min_value,
        max_value,
        id=case_id,
    )
    for (
        value,
        min_value,
        max_value,
        case_id,
    ) in CONVERT_NUMBER_IN_RANGE_OUT_OF_BOUNDS_EXAMPLES
)

CONVERT_NUMBER_IN_RANGE_VALID_ARGS: tuple[
    str,
    ...,
] = (
    "value",
    "min_value",
    "max_value",
    "as_int",
    "as_str",
    "expected",
)
CONVERT_NUMBER_IN_RANGE_VALID_CASES: tuple[
    object,
    ...,
] = tuple(
    pytest.param(
        value,
        min_value,
        max_value,
        as_int,
        as_str,
        expected,
        id=case_id,
    )
    for (
        value,
        min_value,
        max_value,
        as_int,
        as_str,
        expected,
        case_id,
    ) in CONVERT_NUMBER_IN_RANGE_VALID_EXAMPLES
)

FLAG_NAME_ROUNDTRIP_ARGS: tuple[
    str,
    ...,
] = (
    "flag",
    "name",
)
FLAG_NAME_ROUNDTRIP_CASES: tuple[
    object,
    ...,
] = tuple(
    pytest.param(
        flag,
        name,
        id=case_id,
    )
    for (
        flag,
        name,
        case_id,
    ) in FLAG_NAME_ROUNDTRIP_EXAMPLES
)

GET_BATCHES_COUNT_ARGS: tuple[
    str,
    ...,
] = (
    "items",
    "size",
    "expected",
)
GET_BATCHES_COUNT_CASES: tuple[
    object,
    ...,
] = tuple(
    pytest.param(
        items,
        size,
        expected,
        id=case_id,
    )
    for (
        items,
        size,
        expected,
        case_id,
    ) in GET_BATCHES_COUNT_EXAMPLES
)

NORMALIZE_CONDITION_INVALID_ARGS: tuple[
    str,
    ...,
] = (
    "invalid_input",
)
NORMALIZE_CONDITION_INVALID_CASES: tuple[
    object,
    ...,
] = tuple(
    pytest.param(
        invalid_input,
        id=case_id,
    )
    for (
        invalid_input,
        case_id,
    ) in NORMALIZE_CONDITION_INVALID_EXAMPLES
)

NORMALIZE_CONDITION_VALID_ARGS: tuple[
    str,
    ...,
] = (
    "input_str",
    "expected",
)
NORMALIZE_CONDITION_VALID_CASES: tuple[
    object,
    ...,
] = tuple(
    pytest.param(
        input_str,
        expected,
        id=case_id,
    )
    for (
        input_str,
        expected,
        case_id,
    ) in NORMALIZE_CONDITION_VALID_EXAMPLES
)

NORMALIZE_SCALAR_ARGS: tuple[
    str,
    ...,
] = (
    "value",
    "as_str",
    "expected",
)
NORMALIZE_SCALAR_CASES: tuple[
    object,
    ...,
] = tuple(
    pytest.param(
        value,
        as_str,
        (
            expected
            if (
                as_str
                or isinstance(
                    value,
                    (
                        dict,
                        list,
                        tuple,
                    ),
                )
            )
            else value
        ),
        id=f"{case_id}_as_{'string' if as_str else 'value'}",
    )
    for (
        value,
        expected,
        case_id,
    ) in NORMALIZE_SCALAR_EXAMPLES
    for as_str in (
        True,
        False,
    )
)

NORMALIZE_VALID_FIELDS_VALID_ARGS: tuple[
    str,
    ...,
] = (
    "input_str",
    "expected",
)
NORMALIZE_VALID_FIELDS_VALID_CASES: tuple[
    object,
    ...,
] = tuple(
    pytest.param(
        input_str,
        expected,
        id=case_id,
    )
    for (
        input_str,
        expected,
        case_id,
    ) in NORMALIZE_VALID_FIELDS_VALID_EXAMPLES
)

PARSE_VALID_FIELDS_INVALID_ARGS: tuple[
    str,
    ...,
] = (
    "invalid_input",
)
PARSE_VALID_FIELDS_INVALID_CASES: tuple[
    object,
    ...,
] = tuple(
    pytest.param(
        invalid_input,
        id=case_id,
    )
    for (
        invalid_input,
        case_id,
    ) in PARSE_VALID_FIELDS_INVALID_EXAMPLES
)

RE_FULLMATCH_AND_SEARCH_EXTENDED_ARGS: tuple[
    str,
    ...,
] = (
    "pattern",
    "target",
    "expected_fullmatch",
    "expected_search",
)
RE_FULLMATCH_AND_SEARCH_EXTENDED_CASES: tuple[
    object,
    ...,
] = tuple(
    pytest.param(
        pattern,
        target,
        expected_fullmatch,
        expected_search,
        id=(
            f"{case_id}_"
            f"{'fullmatch' if expected_fullmatch else 'no_fullmatch'}_"
            f"{'search' if expected_search else 'no_search'}"
        ),
    )
    for (
        pattern,
        target,
        expected_fullmatch,
        expected_search,
        case_id,
    ) in RE_FULLMATCH_AND_SEARCH_EXAMPLES
)

REL_PATH_ARGS: tuple[
    str,
    ...,
] = (
    "input_path",
)
REL_PATH_CASES: tuple[
    object,
    ...,
] = tuple(
    pytest.param(
        input_path,
        id=case_id,
    )
    for (
        input_path,
        case_id,
    ) in REL_PATH_EXAMPLES
)

VALIDATE_FILE_PATH_SUCCESS_ARGS: tuple[
    str,
    ...,
] = (
    "filename",
    "must_be_file",
)
VALIDATE_FILE_PATH_SUCCESS_CASES: tuple[
    object,
    ...,
] = tuple(
    pytest.param(
        filename,
        must_be_file,
        id=case_id,
    )
    for (
        filename,
        must_be_file,
        case_id,
    ) in VALIDATE_FILE_PATH_SUCCESS_EXAMPLES
)

VALIDATE_PROXY_URL_INVALID_ARGS: tuple[
    str,
    ...,
] = (
    "invalid_input",
)
VALIDATE_PROXY_URL_INVALID_CASES: tuple[
    object,
    ...,
] = tuple(
    pytest.param(
        invalid_input,
        id=case_id,
    )
    for (
        invalid_input,
        case_id,
    ) in VALIDATE_PROXY_URL_INVALID_EXAMPLES
)

VALIDATE_PROXY_URL_VALID_ARGS: tuple[
    str,
    ...,
] = (
    "proxy_url",
    "expected",
)
VALIDATE_PROXY_URL_VALID_CASES: tuple[
    object,
    ...,
] = tuple(
    pytest.param(
        proxy_url,
        expected,
        id=case_id,
    )
    for (
        proxy_url,
        expected,
        case_id,
    ) in VALIDATE_PROXY_URL_VALID_EXAMPLES
)
