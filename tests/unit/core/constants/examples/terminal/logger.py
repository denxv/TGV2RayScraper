from argparse import (
    Namespace,
)

from tests.unit.core.constants.common import (
    DEBUG,
    FORMAT_LOG_TIME,
    INFO,
)

__all__ = [
    "LOG_DEBUG_OBJECT_EXAMPLES",
    "MICROSECOND_FORMATTER_EXAMPLES",
    "SET_CONSOLE_LEVEL_EXAMPLES",
]

LOG_DEBUG_OBJECT_EXAMPLES: tuple[
    tuple[
        str,
        object,
        str,
    ],
    ...,
] = (
    (
        "dict_object",
        {
            "x": 42,
        },
        "type_dict",
    ),
    (
        "float_object",
        3.14,
        "type_float",
    ),
    (
        "int_object",
        99,
        "type_int",
    ),
    (
        "list_object",
        [
            1,
            2,
            3,
        ],
        "type_list",
    ),
    (
        "namespace_object",
        Namespace(
            a=1,
            b="two",
        ),
        "type_namespace",
    ),
    (
        "string_object",
        "hello",
        "type_string",
    ),
    (
        "tuple_object",
        (
            10,
            20,
        ),
        "type_tuple",
    ),
)

MICROSECOND_FORMATTER_EXAMPLES: tuple[
    tuple[
        str,
        str,
    ],
    ...,
] = (
    (
        "%Y-%m-%d %H:%M:%S.%f",
        "custom_format",
    ),
    (
        FORMAT_LOG_TIME,
        "default_format",
    ),
)

SET_CONSOLE_LEVEL_EXAMPLES: tuple[
    tuple[
        bool,
        int,
        int,
        str,
    ],
    ...,
] = (
    (
        True,
        12345,
        DEBUG,
        "debug_forces_debug_level",
    ),
    (
        True,
        INFO,
        DEBUG,
        "debug_mode_overrides_info_level",
    ),
    (
        False,
        DEBUG,
        DEBUG,
        "no_debug_keeps_debug_level",
    ),
    (
        False,
        INFO,
        INFO,
        "no_debug_keeps_info_level",
    ),
)
