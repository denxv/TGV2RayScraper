from __future__ import (
    annotations,
)

from contextlib import (
    contextmanager,
)
from typing import (
    TYPE_CHECKING,
)

from rich.live import (
    Live,
)
from rich.padding import (
    Padding,
)

from core.constants.common import (
    CHANNEL_TABLE_PADDING,
)
from core.constants.templates.debug.channel import (
    TEMPLATE_DEBUG_CHANNEL_STATUS_RESULT,
    TEMPLATE_DEBUG_CHANNEL_UPDATE_RESULT,
)
from core.terminal.console import (
    console,
)
from core.terminal.logger import (
    logger,
)
from core.terminal.tables import (
    create_extract_table,
    create_status_table,
    create_updates_table,
)

__all__ = [
    "render_channel_status",
    "render_channel_update",
    "render_config_extract",
]

if TYPE_CHECKING:
    from rich.console import (
        Console,
    )

    from core.typing import (
        Callable,
        Generator,
    )
    from domain.channel import (
        ChannelStatus,
        ChannelUpdateResult,
    )
    from domain.config import (
        ConfigExtractionResult,
    )


def render_channel_status(
    results: list[ChannelStatus],
    *,
    console: Console = console,
) -> int:
    total_diff = 0
    table = create_status_table()

    for index, result in enumerate(results, start=1):
        total_diff += result.diff_id

        table.add_row(
            str(index),
            result.channel_name,
            f"{result.current_id:,}",
            f"{result.last_id:,}",
            f"{result.diff_id:,}",
        )
        logger.debug(
            msg=TEMPLATE_DEBUG_CHANNEL_STATUS_RESULT.format(
                result=result,
            ),
        )

    console.print(
        Padding(
            table,
            pad=CHANNEL_TABLE_PADDING,
        ),
    )

    return total_diff


@contextmanager
def render_channel_update(
    *,
    console: Console | None = console,
    refresh_per_second: float = 15.0,
    **kwargs: object,
) -> Generator[Callable[[ChannelUpdateResult], int], None, None]:
    index = 1
    table = create_updates_table()

    with Live(
        Padding(
            table,
            pad=CHANNEL_TABLE_PADDING,
        ),
        console=console,
        refresh_per_second=refresh_per_second,
        **kwargs,  # type: ignore[arg-type]
    ) as live:

        def _add_update(result: ChannelUpdateResult) -> int:
            nonlocal index

            logger.debug(
                msg=TEMPLATE_DEBUG_CHANNEL_UPDATE_RESULT.format(
                    result=result,
                ),
            )

            if not result.changed:
                return 0

            table.add_row(
                str(index),
                result.channel_name,
                f"{result.old_last_id:,}",
                f"{result.new_last_id:,}",
            )

            live.refresh()
            index += 1

            return 1

        yield _add_update


def render_config_extract(
    results: list[ConfigExtractionResult],
    *,
    console: Console = console,
) -> None:
    table = create_extract_table()

    sorted_results = sorted(
        results,
        key=lambda result: (
            result.new_found,
            result.total_found,
        ),
    )

    for index, result in enumerate(sorted_results, start=1):
        table.add_row(
            str(index),
            result.channel_name,
            str(result.total_found),
            str(result.new_found),
        )

    console.print(
        Padding(
            table,
            pad=CHANNEL_TABLE_PADDING,
        ),
    )
