from re import (
    compile as re_compile,
)

from core.typing import (
    CompiledRegex,
)

__all__ = [
    "PATTERN_TG_CHANNEL_NAME",
]

PATTERN_TG_CHANNEL_NAME: CompiledRegex = re_compile(
    r"\bhttps?://t\.me/(?:s/)?([\w]{5,32})",
)
