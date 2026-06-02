from rich.console import (
    Console,
)
from rich.theme import (
    Theme,
)

from core.constants.common import (
    LOGGING_THEME,
)

__all__ = [
    "console",
]

console = Console(
    theme=Theme(
        styles=LOGGING_THEME,
    ),
)
