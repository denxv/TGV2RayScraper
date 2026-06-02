import pytest
from rich.console import (
    Console,
)
from rich.progress import (
    Progress,
)

from core.terminal.progress import (
    create_extract_progress,
    progress_add_task,
    progress_remove_task,
    progress_update_task,
)


def test_create_extract_progress_returns_progress() -> None:
    progress = create_extract_progress()

    assert isinstance(progress, Progress)


def test_create_extract_progress_uses_passed_console() -> None:
    custom_console = Console()

    progress = create_extract_progress(
        console=custom_console,
    )

    assert progress.console is custom_console


def test_progress_add_task() -> None:
    progress = create_extract_progress()

    task_id = progress_add_task(
        progress=progress,
        description="Test task",
        total=10,
    )

    task = progress.tasks[task_id]

    assert task.description == "Test task"
    assert task.total == 10


@pytest.mark.asyncio
async def test_progress_remove_task() -> None:
    progress = create_extract_progress()

    task_id = progress_add_task(
        progress=progress,
        description="Task",
    )
    overall_id = progress_add_task(
        progress=progress,
        description="Overall",
        total=10,
    )

    await progress_remove_task(
        progress=progress,
        task_id=task_id,
        overall_task=overall_id,
        remove_delay=0,
    )

    assert task_id not in {
        task.id
        for task in progress.tasks
    }

    overall_task = next(
        task
        for task in progress.tasks
        if task.id == overall_id
    )

    assert overall_task.completed == 1


def test_progress_update_task() -> None:
    progress = create_extract_progress()

    task_id = progress_add_task(
        progress=progress,
        description="Test",
        total=10,
    )

    progress_update_task(
        progress=progress,
        task_id=task_id,
        advance=3,
    )

    task = progress.tasks[task_id]

    assert task.completed == 3
