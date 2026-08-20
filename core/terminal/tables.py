from rich.table import (
    Column,
    Table,
)

from core.constants.locales import (
    TABLE_CHANNELS_STATUS_COLUMN_CHANNEL,
    TABLE_CHANNELS_STATUS_COLUMN_CURRENT_ID,
    TABLE_CHANNELS_STATUS_COLUMN_DIFF,
    TABLE_CHANNELS_STATUS_COLUMN_LAST_ID,
    TABLE_CHANNELS_STATUS_COLUMN_NO,
    TABLE_CHANNELS_STATUS_TITLE,
    TABLE_CHANNELS_UPDATES_COLUMN_CHANNEL,
    TABLE_CHANNELS_UPDATES_COLUMN_NEW_LAST_ID,
    TABLE_CHANNELS_UPDATES_COLUMN_NO,
    TABLE_CHANNELS_UPDATES_COLUMN_OLD_LAST_ID,
    TABLE_CHANNELS_UPDATES_TITLE,
    TABLE_CONFIGS_EXTRACT_COLUMN_CHANNEL,
    TABLE_CONFIGS_EXTRACT_COLUMN_FOUND,
    TABLE_CONFIGS_EXTRACT_COLUMN_NO,
    TABLE_CONFIGS_EXTRACT_COLUMN_TOTAL,
    TABLE_CONFIGS_EXTRACT_TITLE,
)

__all__ = [
    "create_extract_table",
    "create_status_table",
    "create_table",
    "create_updates_table",
]


def create_extract_table() -> Table:
    columns: list[Column] = [
        Column(
            TABLE_CONFIGS_EXTRACT_COLUMN_NO,
            justify="right",
            style="dim",
        ),
        Column(
            TABLE_CONFIGS_EXTRACT_COLUMN_CHANNEL,
            justify="left",
            style="cyan",
        ),
        Column(
            TABLE_CONFIGS_EXTRACT_COLUMN_TOTAL,
            justify="right",
            style="green",
        ),
        Column(
            TABLE_CONFIGS_EXTRACT_COLUMN_FOUND,
            justify="right",
            style="magenta",
        ),
    ]

    return create_table(
        columns,
        title=TABLE_CONFIGS_EXTRACT_TITLE,
    )


def create_status_table() -> Table:
    columns: list[Column] = [
        Column(
            TABLE_CHANNELS_STATUS_COLUMN_NO,
            justify="right",
            style="dim",
        ),
        Column(
            TABLE_CHANNELS_STATUS_COLUMN_CHANNEL,
            justify="left",
            style="cyan",
        ),
        Column(
            TABLE_CHANNELS_STATUS_COLUMN_CURRENT_ID,
            justify="right",
            style="green",
        ),
        Column(
            TABLE_CHANNELS_STATUS_COLUMN_LAST_ID,
            justify="right",
            style="yellow",
        ),
        Column(
            TABLE_CHANNELS_STATUS_COLUMN_DIFF,
            justify="right",
            style="magenta",
        ),
    ]

    return create_table(
        columns,
        title=TABLE_CHANNELS_STATUS_TITLE,
    )


def create_table(
    columns: list[Column],
    **kwargs: object,
) -> Table:
    return Table(*columns, **kwargs)  # type: ignore[arg-type]


def create_updates_table() -> Table:
    columns: list[Column] = [
        Column(
            TABLE_CHANNELS_UPDATES_COLUMN_NO,
            justify="right",
            style="dim",
        ),
        Column(
            TABLE_CHANNELS_UPDATES_COLUMN_CHANNEL,
            justify="left",
            style="cyan",
        ),
        Column(
            TABLE_CHANNELS_UPDATES_COLUMN_OLD_LAST_ID,
            justify="right",
            style="yellow",
        ),
        Column(
            TABLE_CHANNELS_UPDATES_COLUMN_NEW_LAST_ID,
            justify="right",
            style="green",
        ),
    ]

    return create_table(
        columns,
        title=TABLE_CHANNELS_UPDATES_TITLE,
    )
