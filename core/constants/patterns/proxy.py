from re import (
    compile as re_compile,
)

from core.typing import (
    CompiledRegex,
)

__all__ = [
    "PATTERN_PROXY_URL",
]

PATTERN_PROXY_URL: CompiledRegex = re_compile(
    r"(?P<url>"
        r"(?P<protocol>"
            r"https?"
        r"|"
            r"socks5h?"
        r")://"
        r"(?P<body>"
            r"(?:"
                r"(?P<username>[^:@\s]+)"
                r":(?P<password>\S+)@"
            r")?"
            r"(?P<host>"
                r"\[[0-9a-fA-F:]+\]"
            r"|"
                r"[0-9a-zA-Z.-]+"
            r")"
            r":(?P<port>\d{1,5})"
        r")"
    r")",
)
