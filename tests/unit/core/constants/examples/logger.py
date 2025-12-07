from argparse import (
    Namespace,
)

from tests.unit.core.constants.common import (
    FORMAT_LOG_TIME_MICROSECONDS,
)

__all__ = [
    "COLOR_LEVEL_FILTER_EXAMPLES",
    "LOG_DEBUG_OBJECT_EXAMPLES",
    "MICROSECOND_FORMATTER_EXAMPLES",
]

COLOR_LEVEL_FILTER_EXAMPLES: tuple[
    tuple[
        bool,
        str,
    ],
    ...,
] = (
    (
        False,
        "color_disabled",
    ),
    (
        True,
        "color_enabled",
    ),
)

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
        FORMAT_LOG_TIME_MICROSECONDS,
        "default_format",
    ),
)
