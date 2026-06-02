from re import (
    DOTALL,
)
from re import (
    compile as re_compile,
)

from core.typing import (
    CompiledRegex,
)

__all__ = [
    "PATTERN_VMESS_JSON",
]

PATTERN_VMESS_JSON: CompiledRegex = re_compile(
    r"(?P<json>"
        r"{"
            r".*"
        r"}"
    r")",
    DOTALL,
)
