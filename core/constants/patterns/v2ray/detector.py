from re import (
    compile as re_compile,
)

from core.constants.patterns.v2ray.registry import (
    PATTERNS_V2RAY_URLS_BY_PROTOCOL,
)
from core.typing import (
    CompiledRegex,
    RegexPattern,
)

__all__ = [
    "PATTERN_V2RAY_URL_DETECTOR",
]

_REGEX_V2RAY_PROTOCOL_SEPARATOR: RegexPattern = (
    r"(?:"
        r"://"
        r"|"
        r"(?i:"
            r"%3A%2F%2F"
        r")"
    r")"
)
_REGEX_V2RAY_SUPPORTED_PROTOCOLS: RegexPattern = (
    r"|".join(
        PATTERNS_V2RAY_URLS_BY_PROTOCOL,
    )
)
_REGEX_V2RAY_URL_DETECTOR: RegexPattern = (
    r"(?P<url>"
        r"(?P<protocol>"
            rf"{_REGEX_V2RAY_SUPPORTED_PROTOCOLS}"
        r")"
        rf"{_REGEX_V2RAY_PROTOCOL_SEPARATOR}"
        r"(?P<body>"
            r"(?:"
                r"(?!"
                    r"(?i:"
                        rf"{_REGEX_V2RAY_SUPPORTED_PROTOCOLS}"
                    r")"
                    rf"{_REGEX_V2RAY_PROTOCOL_SEPARATOR}"
                r")"
                r"\S"
            r")+"
        r")"
    r")"
)

PATTERN_V2RAY_URL_DETECTOR: CompiledRegex = re_compile(
    pattern=_REGEX_V2RAY_URL_DETECTOR,
)
