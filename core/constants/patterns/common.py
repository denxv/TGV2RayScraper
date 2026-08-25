from re import (
    compile as re_compile,
)

from core.typing import (
    CompiledRegex,
)

__all__ = [
    "PATTERN_CONFIG_FIELD",
    "PATTERN_PARAM_SEPARATOR",
]

PATTERN_CONFIG_FIELD: CompiledRegex = re_compile(
    r"\w+"
    r"(?:"
        r"\.\w+"
    r")*",
)
PATTERN_PARAM_SEPARATOR: CompiledRegex = re_compile(
    r"\s*,\s*"
    r"|"
    r"\s+",
)
