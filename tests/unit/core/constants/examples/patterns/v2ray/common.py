__all__ = [
    "VMESS_JSON_INVALID_EXAMPLES",
    "VMESS_JSON_VALID_EXAMPLES",
]

VMESS_JSON_INVALID_EXAMPLES: tuple[
    tuple[
        str,
        str,
    ],
    ...,
] = (
    (
        "",
        "empty",
    ),
    (
        "{broken",
        "missing_closing",
    ),
    (
        "broken}",
        "missing_opening",
    ),
    (
        "not a json",
        "plain_text",
    ),
    (
        "{",
        "unclosed",
    ),
    (
        "}",
        "unopened",
    ),
)

VMESS_JSON_VALID_EXAMPLES: tuple[
    tuple[
        str,
        str,
        str,
    ],
    ...,
] = (
    (
        '{"ps":"node-{eu}-01"}',
        '{"ps":"node-{eu}-01"}',
        "braces_inside_string",
    ),
    (
        "{{}}",
        "{{}}",
        "double_braces",
    ),
    (
        'prefix {"a":1,"b":2} suffix',
        '{"a":1,"b":2}',
        "json_with_noise",
    ),
    (
        '{"nested":{"x":1}}',
        '{"nested":{"x":1}}',
        "nested_json",
    ),
    (
        '{"add":"example.com","port":443}',
        '{"add":"example.com","port":443}',
        "simple_json",
    ),
)
