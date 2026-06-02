from asyncio import (
    sleep,
)

from rich.console import (
    Console,
)
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TaskID,
    TaskProgressColumn,
    TextColumn,
    TimeRemainingColumn,
)
from rich.table import (
    Column,
)

from core.constants.common import (
    PROGRESS_REMOVE_DELAY_DEFAULT,
)
from core.terminal.console import (
    console,
)

__all__ = [
    "create_extract_progress",
    "progress_add_task",
    "progress_remove_task",
    "progress_update_task",
]


def create_extract_progress(
    *,
    console: Console = console,
    **kwargs: object,
) -> Progress:
    return Progress(
        SpinnerColumn(
            "dots",
            finished_text="[green]✓[/green]",
        ),
        TextColumn("[cyan]{task.description}"),
        BarColumn(bar_width=None),
        TaskProgressColumn(),
        MofNCompleteColumn(
            table_column=Column(
                justify="center",
            ),
        ),
        TimeRemainingColumn(),
        console=console,
        **kwargs,  # type: ignore[arg-type]
    )


def progress_add_task(
    progress: Progress,
    description: str,
    *,
    total: float | None = 0.0,
    **kwargs: object,
) -> TaskID:
    return progress.add_task(
        description,
        total=total,
        **kwargs,  # type: ignore[arg-type]
    )


async def progress_remove_task(
    progress: Progress,
    *,
    task_id: TaskID,
    advance: float = 1.0,
    overall_task: TaskID | None = None,
    remove_delay: float = PROGRESS_REMOVE_DELAY_DEFAULT,
) -> None:
    if overall_task is not None:
        progress.advance(
            overall_task,
            advance=advance,
        )

    await sleep(remove_delay)
    progress.remove_task(task_id)


def progress_update_task(
    progress: Progress,
    *,
    task_id: TaskID,
    advance: float | None = 1.0,
    **kwargs: object,
) -> None:
    progress.update(
        task_id,
        advance=advance,
        **kwargs,  # type: ignore[arg-type]
    )
