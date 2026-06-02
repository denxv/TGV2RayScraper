from rich.console import (
    Console,
)

from core.terminal.console import (
    console,
)


def test_console_is_console_instance() -> None:
    assert isinstance(console, Console)
