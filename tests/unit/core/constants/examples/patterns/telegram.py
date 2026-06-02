__all__ = [
    "TG_CHANNEL_NAME_INVALID_EXAMPLES",
    "TG_CHANNEL_NAME_VALID_EXAMPLES",
]

TG_CHANNEL_NAME_INVALID_EXAMPLES: tuple[
    tuple[
        str,
        str,
    ],
    ...,
] = (
    (
        "https://t.me/s/",
        "empty_s_variant",
    ),
    (
        "https://t.me/",
        "empty_username",
    ),
    (
        "random text",
        "no_url",
    ),
    (
        "https://t.me/s/abc",
        "too_short_username",
    ),
    (
        "https://telegram.me/mychannel",
        "wrong_domain",
    ),
)

TG_CHANNEL_NAME_VALID_EXAMPLES: tuple[
    tuple[
        str,
        str,
        str,
    ],
    ...,
] = (
    (
        "https://t.me/username/12345",
        "username",
        "channel_with_post",
    ),
    (
        "https://t.me/username?before=12345",
        "username",
        "channel_with_query",
    ),
    (
        "https://t.me/s/username/12345",
        "username",
        "channel_with_s_and_post",
    ),
    (
        "https://t.me/username",
        "username",
        "simple_channel",
    ),
    (
        "https://t.me/s/username",
        "username",
        "simple_channel_with_s",
    ),
)
