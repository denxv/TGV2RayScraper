from argparse import (
    Namespace,
)
from base64 import (
    b64encode,
    urlsafe_b64encode,
)
from json import (
    dumps,
)
from pathlib import (
    Path,
)

from core.typing import (
    Iterable,
    Sized,
)
from tests.unit.core.constants.common import (
    DEFAULT_PATH_PROJECT,
    DEFAULT_PROXY_URL,
)

__all__ = [
    "ABS_PATH_ABSOLUTE_EXAMPLES",
    "ABS_PATH_INVALID_TYPE_EXAMPLES",
    "ABS_PATH_RELATIVE_EXAMPLES",
    "B64DECODE_SAFE_INVALID_INPUTS_EXAMPLES",
    "B64DECODE_SAFE_VALID_AND_INVALID_EXAMPLES",
    "B64ENCODE_SAFE_INVALID_TYPE_EXAMPLES",
    "B64ENCODE_SAFE_VALID_EXAMPLES",
    "BATCHED_EXAMPLES",
    "COLLECT_ARGS_COMBINED_EXAMPLES",
    "CONVERT_NUMBER_IN_RANGE_INVALID_VALUE_EXAMPLES",
    "CONVERT_NUMBER_IN_RANGE_OUT_OF_BOUNDS_EXAMPLES",
    "CONVERT_NUMBER_IN_RANGE_VALID_EXAMPLES",
    "FLAG_NAME_ROUNDTRIP_EXAMPLES",
    "GET_BATCHES_COUNT_EXAMPLES",
    "NORMALIZE_CONDITION_INVALID_EXAMPLES",
    "NORMALIZE_CONDITION_VALID_EXAMPLES",
    "NORMALIZE_SCALAR_EXAMPLES",
    "NORMALIZE_VALID_FIELDS_VALID_EXAMPLES",
    "PARSE_VALID_FIELDS_INVALID_EXAMPLES",
    "REL_PATH_EXAMPLES",
    "RE_FULLMATCH_AND_SEARCH_EXAMPLES",
    "VALIDATE_FILE_PATH_SUCCESS_EXAMPLES",
    "VALIDATE_PROXY_URL_INVALID_EXAMPLES",
    "VALIDATE_PROXY_URL_VALID_EXAMPLES",
]

ABS_PATH_ABSOLUTE_EXAMPLES: tuple[
    tuple[
        str,
        str,
    ],
    ...,
] = (
    (
        str(
            Path.home().resolve(),
        ),
        "home_path",
    ),
    (
        "/etc/default",
        "etc_default",
    ),
    (
        str(
            Path("/usr/local/bin").resolve(),
        ),
        "usr_local_bin",
    ),
)

ABS_PATH_INVALID_TYPE_EXAMPLES: tuple[
    tuple[
        object,
        str,
    ],
    ...,
] = (
    (
        {
            "a": 1,
        },
        "type_dict",
    ),
    (
        123,
        "type_int",
    ),
    (
        [
            1,
            2,
            3,
        ],
        "type_list",
    ),
    (
        None,
        "type_none",
    ),
    (
        object(),
        "type_object",
    ),
)

ABS_PATH_RELATIVE_EXAMPLES: tuple[
    tuple[
        str,
        str,
    ],
    ...,
] = (
    (
        "../backup/",
        "backup_relative",
    ),
    (
        "channels/current.json",
        "channels_current",
    ),
    (
        "configs/v2ray-clean.txt",
        "configs_v2ray_clean",
    ),
    (
        "./data/../data",
        "data_relative",
    ),
    (
        "logs/",
        "logs",
    ),
)

B64DECODE_SAFE_INVALID_INPUTS_EXAMPLES: tuple[
    tuple[
        object,
        str,
    ],
    ...,
] = (
    (
        "a=",
        "bad_padding",
    ),
    (
        "###$$$",
        "nonsensical",
    ),
    (
        b"bytes",
        "type_bytes",
    ),
    (
        {
            "dict": 1,
        },
        "type_dict",
    ),
    (
        123,
        "type_int",
    ),
    (
        [
            "list",
        ],
        "type_list",
    ),
    (
        None,
        "type_none",
    ),
)

B64DECODE_SAFE_VALID_AND_INVALID_EXAMPLES: tuple[
    tuple[
        str,
        str,
        str,
    ],
    ...,
] = (
    (
        "",
        "",
        "empty_string",
    ),
    (
        "$$$%%%!!!",
        "",
        "invalid_b64_string",
    ),
    (
        b64encode(b"\xff\xfe\xfd").decode(),
        "���",
        "invalid_utf8_bytes",
    ),
    (
        b64encode(b"hello").decode(),
        "hello",
        "missing_padding",
    ),
    (
        b64encode(b"data").decode().rstrip("="),
        "data",
        "standard_base64",
    ),
    (
        f"  {b64encode(b'trim').decode()}  ",
        "trim",
        "trim_spaces",
    ),
    (
        urlsafe_b64encode(b"test123").decode(),
        "test123",
        "urlsafe_base64",
    ),
)

B64ENCODE_SAFE_INVALID_TYPE_EXAMPLES: tuple[
    tuple[
        object,
        str,
    ],
    ...,
] = (
    (
        b"bytes",
        "type_bytes",
    ),
    (
        {
            "dict": 1,
        },
        "type_dict",
    ),
    (
        123,
        "type_int",
    ),
    (
        [
            "list",
        ],
        "type_list",
    ),
    (
        None,
        "type_none",
    ),
)

B64ENCODE_SAFE_VALID_EXAMPLES: tuple[
    tuple[
        str,
        str,
        str,
    ],
    ...,
] = (
    (
        "hello",
        b64encode(b"hello").decode(),
        "ascii_text",
    ),
    (
        "Привет",
        b64encode("Привет".encode()).decode(),
        "cyrillic_text",
    ),
    (
        "",
        b64encode(b"").decode(),
        "empty_string",
    ),
    (
        "こんにちは",
        b64encode("こんにちは".encode()).decode(),
        "japanese_text",
    ),
    (
        "with space!",
        b64encode(b"with space!").decode(),
        "text_with_space",
    ),
)

BATCHED_EXAMPLES: tuple[
    tuple[
        Iterable[int],
        int,
        list[tuple[int, ...]],
        str,
    ],
    ...,
] = (
    (
        [],
        3,
        [],
        "empty_iterable",
    ),
    (
        [1, 2, 3, 4],
        2,
        [(1, 2), (3, 4)],
        "even_batches",
    ),
    (
        [1, 2, 3, 4, 5],
        2,
        [(1, 2), (3, 4), (5,)],
        "last_partial_batch",
    ),
    (
        [1, 2, 3],
        -5,
        [(1,), (2,), (3,)],
        "negative_size_fallback_to_one",
    ),
    (
        [1, 2, 3],
        10,
        [(1, 2, 3)],
        "size_larger_than_iterable",
    ),
    (
        [1, 2, 3],
        0,
        [(1,), (2,), (3,)],
        "zero_size_fallback_to_one",
    ),
)

COLLECT_ARGS_COMBINED_EXAMPLES: tuple[
    tuple[
        Namespace,
        list[str],
        list[object],
        str,
    ],
    ...,
] = (
    (
        Namespace(
            no_async=False,
            reverse=True,
        ),
        [
            "--no_async",
            "--reverse",
        ],
        [
            "--reverse",
        ],
        "flag_with_underscores",
    ),
    (
        Namespace(
            include=[
                "a",
                "b",
                "c",
            ],
            params={
                "a": 1,
            },
        ),
        [
            "--include",
            "--params",
        ],
        [
            "--include",
            [
                "a",
                "b",
                "c",
            ],
            "--params",
            {
                "a": 1,
            },
        ],
        "list_and_dict_values",
    ),
    (
        Namespace(),
        [
            "--missing",
        ],
        [],
        "missing_attr",
    ),
    (
        Namespace(
            config=None,
            const="",
            dry_run=False,
            output="log.txt",
            retry=0,
            threshold=0.1,
            verbose=True,
        ),
        [
            "--const",
            "--config",
            "--dry-run",
            "--output",
            "--retry",
            "--threshold",
            "--verbose",
        ],
        [
            "--const",
            "--output",
            "log.txt",
            "--retry",
            0,
            "--threshold",
            0.1,
            "--verbose",
        ],
        "mixed_types",
    ),
    (
        Namespace(
            test_special_case=True,
        ),
        [
            "----test-special_case",
        ],
        [
            "--test-special-case",
        ],
        "quadruple_dash_flag",
    ),
    (
        Namespace(
            weird_flag=True,
        ),
        [
            "---weird-flag",
        ],
        [
            "--weird-flag",
        ],
        "triple_dash_flag",
    ),
)

CONVERT_NUMBER_IN_RANGE_INVALID_VALUE_EXAMPLES: tuple[
    tuple[
        str | None,
        str,
    ],
    ...,
] = (
    (
        "5,5",
        "comma_in_number",
    ),
    (
        "7..2",
        "double_dot",
    ),
    (
        "",
        "empty_str",
    ),
    (
        "abc",
        "non_numeric_str",
    ),
    (
        None,
        "none_value",
    ),
)

CONVERT_NUMBER_IN_RANGE_OUT_OF_BOUNDS_EXAMPLES: tuple[
    tuple[
        str,
        int,
        int,
        str,
    ],
    ...,
] = (
    (
        "111",
        0,
        100,
        "above_max1",
    ),
    (
        "1234",
        500,
        1000,
        "above_max2",
    ),
    (
        "-10",
        0,
        10,
        "below_min1",
    ),
    (
        "-500",
        -300,
        300,
        "below_min2",
    ),
)

CONVERT_NUMBER_IN_RANGE_VALID_EXAMPLES: tuple[
    tuple[
        str,
        int,
        int,
        bool,
        bool,
        float | int | str,
        str,
    ],
    ...,
] = (
    (
        "5.5",
        0,
        10,
        False,
        False,
        5.5,
        "float_middle",
    ),
    (
        "0.0",
        0,
        10,
        False,
        False,
        0.0,
        "float_min",
    ),
    (
        "10.0",
        0,
        10,
        False,
        False,
        10.0,
        "float_max",
    ),
    (
        "5",
        0,
        10,
        True,
        False,
        5,
        "int_middle",
    ),
    (
        "0",
        0,
        10,
        True,
        False,
        0,
        "int_min",
    ),
    (
        "10",
        0,
        10,
        True,
        False,
        10,
        "int_max",
    ),
    (
        "7",
        0,
        10,
        True,
        True,
        "7",
        "str_int",
    ),
    (
        "3.14",
        0,
        10,
        False,
        True,
        "3.14",
        "str_float",
    ),
)

FLAG_NAME_ROUNDTRIP_EXAMPLES: tuple[
    tuple[
        str,
        str,
        str,
    ],
    ...,
] = (
    (
        "--verbose",
        "verbose",
        "double_dash",
    ),
    (
        "----multi--dash",
        "multi__dash",
        "double_inner_dash",
    ),
    (
        "--with_underscore",
        "with_underscore",
        "existing_underscore",
    ),
    (
        "--dry-run",
        "dry_run",
        "inner_dash",
    ),
    (
        "--step1",
        "step1",
        "number_in_name",
    ),
    (
        "-a",
        "a",
        "single_dash",
    ),
    (
        "---weird-flag",
        "weird_flag",
        "triple_dash",
    ),
)

GET_BATCHES_COUNT_EXAMPLES: tuple[
    tuple[
        Sized,
        int,
        int,
        str,
    ],
    ...,
] = (
    (
        [],
        3,
        0,
        "empty_items",
    ),
    (
        [1, 2, 3, 4],
        2,
        2,
        "even_division",
    ),
    (
        [1, 2, 3],
        -2,
        3,
        "negative_size_fallback_to_one",
    ),
    (
        [1, 2, 3, 4, 5],
        2,
        3,
        "rounded_up",
    ),
    (
        [1, 2, 3],
        10,
        1,
        "size_larger_than_items",
    ),
    (
        [1, 2, 3],
        0,
        3,
        "zero_size_fallback_to_one",
    ),
)

NORMALIZE_CONDITION_INVALID_EXAMPLES: tuple[
    tuple[
        str,
        str,
    ],
    ...,
] = (
    (
        "",
        "empty_string",
    ),
    (
        "\n",
        "newline_only",
    ),
    (
        "   ",
        "spaces_only",
    ),
    (
        "\t",
        "tab_only",
    ),
)

NORMALIZE_CONDITION_VALID_EXAMPLES: tuple[
    tuple[
        str,
        str,
        str,
    ],
    ...,
] = (
    (
        "host == 1.1.1.1 and port > 1000",
        "host == 1.1.1.1 and port > 1000",
        "complex_condition",
    ),
    (
        "host   ==    1.1.1.1",
        "host   ==    1.1.1.1",
        "multiple_spaces",
    ),
    (
        "   host==1.1.1.1   ",
        "host==1.1.1.1",
        "no_spaces_expression",
    ),
    (
        "host == 1.1.1.1",
        "host == 1.1.1.1",
        "simple_condition",
    ),
    (
        "  host == 1.1.1.1  ",
        "host == 1.1.1.1",
        "strip_spaces",
    ),
    (
        "\thost\t==\t1.1.1.1\t",
        "host\t==\t1.1.1.1",
        "tabs",
    ),
)

NORMALIZE_SCALAR_EXAMPLES: tuple[
    tuple[
        object,
        str | None,
        str,
    ],
    ...,
] = (
    (
        {
            "b": 2,
            "a": 1,
        },
        dumps(
            obj={
                "b": 2,
                "a": 1,
            },
            sort_keys=True,
            separators=(",", ":"),
        ),
        "dict",
    ),
    (
        3.14,
        "3.14",
        "float",
    ),
    (
        42,
        "42",
        "int",
    ),
    (
        [
            1,
            2,
            3,
        ],
        dumps(
            obj=[
                1,
                2,
                3,
            ],
            sort_keys=True,
            separators=(",", ":"),
        ),
        "list",
    ),
    (
        None,
        None,
        "none",
    ),
    (
        "hello",
        "hello",
        "str",
    ),
    (
        (
            1,
            2,
            3,
        ),
        dumps(
            obj=(
                1,
                2,
                3,
            ),
            sort_keys=True,
            separators=(",", ":"),
        ),
        "tuple",
    ),
)

NORMALIZE_VALID_FIELDS_VALID_EXAMPLES: tuple[
    tuple[
        str,
        str,
        str,
    ],
    ...,
] = (
    (
        "a1,b2,c3",
        "a1,b2,c3",
        "comma_only",
    ),
    (
        "",
        "",
        "empty",
    ),
    (
        "a1, b2 c3",
        "a1,b2,c3",
        "mixed_sep",
    ),
    (
        "field1",
        "field1",
        "single_field",
    ),
    (
        "a1 b2 c3",
        "a1,b2,c3",
        "space_only",
    ),
    (
        "field1 , field2 ",
        "field1,field2",
        "spaces_around",
    ),
    (
        "   ",
        "",
        "spaces_only",
    ),
    (
        "_field1 field_2",
        "_field1,field_2",
        "underscores",
    ),
    (
        "F1,F2 F3",
        "F1,F2,F3",
        "uppercase",
    ),
)

PARSE_VALID_FIELDS_INVALID_EXAMPLES: tuple[
    tuple[
        object,
        str,
    ],
    ...,
] = (
    (
        "field1,field1",
        "duplicate_field",
    ),
    (
        "field1,,field2",
        "empty_between_commas",
    ),
    (
        "field1,",
        "empty_end",
    ),
    (
        ",field1",
        "empty_start",
    ),
    (
        "field@",
        "invalid_at",
    ),
    (
        "field!name",
        "invalid_exclaim",
    ),
    (
        "123-invalid",
        "invalid_start_digit",
    ),
    (
        " , , ",
        "only_empty_spaces",
    ),
    (
        {
            "a": 1,
        },
        "type_dict",
    ),
    (
        123,
        "type_int",
    ),
    (
        [
            "a",
            "b",
        ],
        "type_list",
    ),
    (
        None,
        "type_none",
    ),
)

RE_FULLMATCH_AND_SEARCH_EXAMPLES: tuple[
    tuple[
        str,
        object,
        bool,
        bool,
        str,
    ],
    ...,
] = (
    (
        r"(?i)true|false",
        False,
        True,
        True,
        "bool_false",
    ),
    (
        r"(?i)true|false",
        True,
        True,
        True,
        "bool_true",
    ),
    (
        r".*",
        "",
        True,
        True,
        "empty_string",
    ),
    (
        r"\d+\.\d+",
        3.14,
        True,
        True,
        "float_value",
    ),
    (
        r"\d+",
        "123",
        True,
        True,
        "full_digits_match",
    ),
    (
        r"\d+",
        456,
        True,
        True,
        "int_value",
    ),
    (
        r"[a-z]+\s\d+",
        "abc123",
        False,
        False,
        "letters_no_space_digits",
    ),
    (
        r"[a-z]+\s\d+",
        "abc 123",
        True,
        True,
        "letters_space_digits",
    ),
    (
        r"\d+[a-z]+",
        "123abc",
        True,
        True,
        "mixed_digits_letters",
    ),
    (
        r"\d+[a-z]+",
        "123abcXYZ",
        False,
        True,
        "mixed_digits_letters_extra",
    ),
    (
        r"None",
        None,
        True,
        True,
        "none_value",
    ),
    (
        r"\S+",
        "   ",
        False,
        False,
        "non_space_only",
    ),
    (
        r"\d+",
        "123abc",
        False,
        True,
        "partial_digits_mismatch",
    ),
    (
        r"\w+",
        "  abc  ",
        False,
        True,
        "spaces_fullmatch_fail",
    ),
    (
        r"\s+",
        "   ",
        True,
        True,
        "spaces_only",
    ),
    (
        r"[!@#]+",
        "!@#",
        True,
        True,
        "special_chars_exact",
    ),
    (
        r"[!@#]+",
        "!@#abc",
        False,
        True,
        "special_chars_extra",
    ),
    (
        r"abc",
        "abc",
        True,
        True,
        "string_abc",
    ),
    (
        r"abc",
        "abcd",
        False,
        True,
        "string_abcd",
    ),
    (
        r"[a-zA-Z_]+",
        "_varName",
        True,
        True,
        "underscore_var",
    ),
    (
        r"[a-zA-Z_]+",
        "_var123",
        False,
        True,
        "underscore_var_with_digits",
    ),
)

REL_PATH_EXAMPLES: tuple[
    tuple[
        str,
        str,
    ],
    ...,
] = (
    (
        "/etc/default",
        "absolute_outside_etc_default",
    ),
    (
        str(Path.home().resolve()),
        "absolute_outside_home",
    ),
    (
        str(Path("/usr/local/bin").resolve()),
        "absolute_outside_usr_local_bin",
    ),
    (
        str(DEFAULT_PATH_PROJECT / "channels/current.json"),
        "absolute_inside_channels",
    ),
    (
        str(DEFAULT_PATH_PROJECT / "configs/v2ray-clean.txt"),
        "absolute_inside_configs",
    ),
    (
        str(DEFAULT_PATH_PROJECT / "logs/"),
        "absolute_inside_logs",
    ),
    (
        "../backup/",
        "relative_backup",
    ),
    (
        "channels/current.json",
        "relative_channels",
    ),
    (
        "configs/v2ray-clean.txt",
        "relative_configs",
    ),
    (
        "./configs/../configs/v2ray-clean.txt",
        "relative_mixed",
    ),
    (
        "../../other_dir/file.txt",
        "relative_outside_other_dir",
    ),
    (
        "../some_folder/file.txt",
        "relative_outside_some_folder",
    ),
    (
        ".",
        "root_itself",
    ),
)

VALIDATE_FILE_PATH_SUCCESS_EXAMPLES: tuple[
    tuple[
        str,
        bool,
        str,
    ],
    ...,
] = (
    (
        "file.txt",
        True,
        "file_exists",
    ),
    (
        "new_file.txt",
        False,
        "file_missing_must_be_file_false",
    ),
)

VALIDATE_PROXY_URL_INVALID_EXAMPLES: tuple[
    tuple[
        object,
        str,
    ],
    ...,
] = (
    (
        "",
        "empty_string",
    ),
    (
        "http://host#name:8080",
        "invalid_char_in_host",
    ),
    (
        "http://user name:pass word@127.0.0.1:10808",
        "malformed_auth_with_spaces",
    ),
    (
        "http://:8080",
        "missing_host",
    ),
    (
        "http://",
        "missing_host_and_port",
    ),
    (
        "http://user@localhost:8080",
        "missing_password",
    ),
    (
        "http://localhost",
        "missing_port",
    ),
    (
        "http://hostname:",
        "missing_port_value",
    ),
    (
        "http://:password@host:8080",
        "missing_username",
    ),
    (
        "http://localhost:-80",
        "negative_port",
    ),
    (
        "not_a_url",
        "no_protocol",
    ),
    (
        "http://localhost:8080/extra",
        "path_not_allowed",
    ),
    (
        "http://localhost:abc",
        "port_not_numeric",
    ),
    (
        "http://localhost:99999",
        "port_too_high",
    ),
    (
        "http://localhost:0",
        "port_zero",
    ),
    (
        "http://localhost:8080?query=1",
        "query_not_allowed",
    ),
    (
        "http://us er:pass@host:8080",
        "space_in_username",
    ),
    (
        "http://user:pa ss@host:8080",
        "space_in_password",
    ),
    (
        "http://host name:8080",
        "space_in_host",
    ),
    (
        {},
        "type_dict",
    ),
    (
        123,
        "type_int",
    ),
    (
        [],
        "type_list",
    ),
    (
        None,
        "type_none",
    ),
    (
        object(),
        "type_object",
    ),
    (
        "http://my_proxy:8080",
        "underscore_in_host",
    ),
    (
        "ftp://proxy.com:8080",
        "unsupported_protocol_ftp",
    ),
    (
        "socks4://proxy.com:8080",
        "unsupported_protocol_socks4",
    ),
    (
        "tcp://proxy.com:8080",
        "unsupported_protocol_tcp",
    ),
    (
        "   ",
        "whitespace_only",
    ),
)

VALIDATE_PROXY_URL_VALID_EXAMPLES: tuple[
    tuple[
        str,
        str,
        str,
    ],
    ...,
] = (
    (
        DEFAULT_PROXY_URL,
        DEFAULT_PROXY_URL,
        "default_proxy_url",
    ),
    (
        "http://proxy.example.com:8080",
        "http://proxy.example.com:8080",
        "http_domain_no_auth",
    ),
    (
        "http://admin:s3cret@proxy.local:3128",
        "http://admin:s3cret@proxy.local:3128",
        "http_domain_with_auth",
    ),
    (
        "  http://127.0.0.1:8080  ",
        "http://127.0.0.1:8080",
        "http_ipv4_both_spaces",
    ),
    (
        "  http://127.0.0.1:8080",
        "http://127.0.0.1:8080",
        "http_ipv4_leading_space",
    ),
    (
        "http://127.0.0.1:8888",
        "http://127.0.0.1:8888",
        "http_ipv4_no_auth",
    ),
    (
        "http://127.0.0.1:8080  ",
        "http://127.0.0.1:8080",
        "http_ipv4_trailing_space",
    ),
    (
        "http://user:pass@127.0.0.1:8888",
        "http://user:pass@127.0.0.1:8888",
        "http_ipv4_with_auth",
    ),
    (
        "http://localhost:3128",
        "http://localhost:3128",
        "http_localhost_no_auth",
    ),
    (
        "https://user:p@ss:w0rd@secure.com:443",
        "https://user:p@ss:w0rd@secure.com:443",
        "https_complex_password",
    ),
    (
        "https://secure-proxy.com:443",
        "https://secure-proxy.com:443",
        "https_domain_no_auth",
    ),
    (
        "https://192.168.1.1:8443",
        "https://192.168.1.1:8443",
        "https_ipv4_no_auth",
    ),
    (
        "socks5://proxy.com:1080",
        "socks5://proxy.com:1080",
        "socks5_domain_no_auth",
    ),
    (
        "socks5://user:pass@proxy.com:1080",
        "socks5://user:pass@proxy.com:1080",
        "socks5_domain_with_auth",
    ),
    (
        "socks5://[::1]:1080",
        "socks5://[::1]:1080",
        "socks5_ipv6_no_auth",
    ),
    (
        "socks5://user:pass@[::1]:1080",
        "socks5://user:pass@[::1]:1080",
        "socks5_ipv6_with_auth",
    ),
    (
        "socks5h://tor-proxy.local:9050",
        "socks5h://tor-proxy.local:9050",
        "socks5h_domain_no_auth",
    ),
    (
        "socks5h://alice:wonderland@tor.net:9050",
        "socks5h://alice:wonderland@tor.net:9050",
        "socks5h_domain_with_auth",
    ),
    (
        "socks5h://[2001:db8::1]:1080",
        "socks5h://[2001:db8::1]:1080",
        "socks5h_ipv6_no_auth",
    ),
    (
        "socks5h://user:pass@[2001:db8::1]:1080",
        "socks5h://user:pass@[2001:db8::1]:1080",
        "socks5h_ipv6_with_auth",
    ),
)
