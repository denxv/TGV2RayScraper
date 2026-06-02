from rich.table import (
    Column,
    Table,
)

from core.terminal.tables import (
    create_extract_table,
    create_status_table,
    create_table,
    create_updates_table,
)


def test_create_extract_table() -> None:
    table = create_extract_table()

    assert isinstance(table, Table)
    assert table.title == "Configs Extract"

    headers = [
        column.header
        for column in table.columns
    ]

    assert headers == [
        "No",
        "Channel",
        "Total",
        "Found",
    ]


def test_create_status_table() -> None:
    table = create_status_table()

    assert isinstance(table, Table)
    assert table.title == "Channels Status"

    headers = [
        column.header
        for column in table.columns
    ]

    assert headers == [
        "No",
        "Channel",
        "Current ID",
        "Last ID",
        "Diff",
    ]


def test_create_table() -> None:
    columns = [
        Column("Test"),
    ]

    table = create_table(
        columns=columns,
        title="Test Table",
    )

    assert isinstance(table, Table)
    assert table.title == "Test Table"
    assert len(table.columns) == 1
    assert table.columns[0].header == "Test"


def test_create_updates_table() -> None:
    table = create_updates_table()

    assert isinstance(table, Table)
    assert table.title == "Channels Updates"

    headers = [
        column.header
        for column in table.columns
    ]

    assert headers == [
        "No",
        "Channel",
        "Old Last ID",
        "New Last ID",
    ]
