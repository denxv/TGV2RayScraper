from rich.table import (
    Column,
    Table,
)

__all__ = [
    "create_extract_table",
    "create_status_table",
    "create_table",
    "create_updates_table",
]


def create_extract_table() -> Table:
    columns = [
        Column("No", justify="right", style="dim"),
        Column("Channel", justify="left", style="cyan"),
        Column("Total", justify="right", style="green"),
        Column("Found", justify="right", style="magenta"),
    ]

    return create_table(
        columns,
        title="Configs Extract",
    )


def create_status_table() -> Table:
    columns = [
        Column("No", justify="right", style="dim"),
        Column("Channel", justify="left", style="cyan"),
        Column("Current ID", justify="right", style="green"),
        Column("Last ID", justify="right", style="yellow"),
        Column("Diff", justify="right", style="magenta"),
    ]

    return create_table(
        columns,
        title="Channels Status",
    )


def create_table(
    columns: list[Column],
    **kwargs: object,
) -> Table:
    return Table(*columns, **kwargs)  # type: ignore[arg-type]


def create_updates_table() -> Table:
    columns = [
        Column("No", justify="right", style="dim"),
        Column("Channel", justify="left", style="cyan"),
        Column("Old Last ID", justify="right", style="yellow"),
        Column("New Last ID", justify="right", style="green"),
    ]

    return create_table(
        columns,
        title="Channels Updates",
    )
