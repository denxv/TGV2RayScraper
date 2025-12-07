__all__ = [
    "STATUS_TRACKING_COMBINED_EXAMPLES",
]

STATUS_TRACKING_COMBINED_EXAMPLES: tuple[
    tuple[
        tuple[
            dict[str, int],
            ...,
        ],
        dict[str, object],
        dict[str, int],
        bool,
        bool,
        str,
    ],
    ...,
] = (
    (
        (
            {
                "a": 1,
            },
        ),
        {},
        {
            "a": 1,
            "b": 2,
        },
        False,
        False,
        "track_args_false_dict",
    ),
    (
        (
            {
                "x": 1,
                "y": 2,
            },
        ),
        {},
        {
            "x": 1,
        },
        False,
        False,
        "track_args_false_remove",
    ),
    (
        (
            {
                "a": 1,
            },
        ),
        {},
        {
            "a": 1,
            "b": 2,
        },
        True,
        True,
        "track_args_true_add_one",
    ),
    (
        (
            {
                "k": 0,
            },
        ),
        {},
        {
            "k": 0,
            "1": 1,
            "2": 2,
        },
        True,
        True,
        "track_args_true_add_two",
    ),
    (
        (
            {},
        ),
        {},
        {},
        True,
        True,
        "track_args_true_empty",
    ),
    (
        (
            {
                "x": 1,
                "y": 2,
            },
        ),
        {},
        {
            "x": 1,
        },
        True,
        True,
        "track_args_true_remove",
    ),
    (
        (),
        {
            "data": {
                "a": 1,
            },
        },
        {
            "a": 1,
            "b": 2,
        },
        False,
        False,
        "track_kwargs_false_dict",
    ),
    (
        (),
        {
            "data": {
                "key": 100,
            },
        },
        {
            "k": 0,
            "1": 1,
            "2": 2,
        },
        True,
        True,
        "track_kwargs_true_add_two",
    ),
    (
        (),
        {
            "data": {
                "a": 1,
            },
        },
        {
            "a": 1,
            "b": 2,
        },
        True,
        True,
        "track_kwargs_true_dict",
    ),
    (
        (),
        {
            "data": {},
            "dict": {},
        },
        {},
        True,
        True,
        "track_kwargs_true_empty",
    ),
    (
        (),
        {
            "int": 42,
            "data": {
                "x": 1,
            },
        },
        {
            "y": 22,
        },
        True,
        False,
        "track_kwargs_true_int_first_arg",
    ),
    (
        (),
        {
            "str": "string",
        },
        {
            "x": 1,
            "y": 2,
        },
        True,
        False,
        "track_kwargs_true_str_first_arg",
    ),
)
