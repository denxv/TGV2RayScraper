from core.typing import (
    MessageStr,
)

__all__ = [
    "MESSAGE_ERROR_CONDITION_EMPTY",
    "MESSAGE_ERROR_NO_FIELDS_PROVIDED",
    "MESSAGE_ERROR_NO_POSTS_FOUND",
    "MESSAGE_ERROR_PROXY_EMPTY",
    "MESSAGE_ERROR_SSR_MISSING_BASE64",
    "MESSAGE_ERROR_UNEXPECTED_FAILURE",
]

MESSAGE_ERROR_CONDITION_EMPTY: MessageStr = (
    "The condition cannot be empty."
)
MESSAGE_ERROR_NO_FIELDS_PROVIDED: MessageStr = (
    "No fields were provided."
)
MESSAGE_ERROR_NO_POSTS_FOUND: MessageStr = (
    "No posts were found."
)
MESSAGE_ERROR_PROXY_EMPTY: MessageStr = (
    "The proxy URL cannot be empty."
)
MESSAGE_ERROR_SSR_MISSING_BASE64: MessageStr = (
    "SSR configuration is missing base64 data."
)
MESSAGE_ERROR_UNEXPECTED_FAILURE: MessageStr = (
    "An unexpected failure occurred. Please try again."
)
