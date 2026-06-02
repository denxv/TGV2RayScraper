from re import (
    compile as re_compile,
)

from core.typing import (
    CompiledRegex,
)

__all__ = [
    "PATTERN_V2RAY_URL_DETECTOR",
]

PATTERN_V2RAY_URL_DETECTOR: CompiledRegex = re_compile(
    r"(?P<url>"
        r"(?P<protocol>"
            r"anytls"
        r"|"
            r"hy2"
        r"|"
            r"hysteria2"
        r"|"
            r"ss"
        r"|"
            r"ssr"
        r"|"
            r"trojan"
        r"|"
            r"tuic"
        r"|"
            r"vless"
        r"|"
            r"vmess"
        r"|"
            r"wireguard"
        r")://"
        r"(?P<body>"
            r"(?:"
                r"(?!"
                    r"://"
                r"|"
                    r"(?:"
                        r"anytls"
                    r"|"
                        r"hy2"
                    r"|"
                        r"hysteria2"
                    r"|"
                        r"ss"
                    r"|"
                        r"ssr"
                    r"|"
                        r"trojan"
                    r"|"
                        r"tuic"
                    r"|"
                        r"vless"
                    r"|"
                        r"vmess"
                    r"|"
                        r"wireguard"
                    r")://"
                r")\S"
            r")+"
        r")"
    r")",
)
