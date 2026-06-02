from datetime import (
    datetime,
    timezone,
)
from logging import (
    getLogger,
)
from pathlib import (
    Path,
)
from unittest.mock import (
    Mock,
)

import pytest
from _pytest.config import (
    Config,
)
from _pytest.nodes import (
    Item,
)
from pytest_mock import (
    MockerFixture,
)

from core.constants.common import (
    DEFAULT_LOGGER_NAME,
)
from core.terminal.logger import (
    Logger,
    log_debug_object,
)


def _create_file(
    path: Path,
    *,
    should_create: bool = True,
) -> Path:
    if should_create:
        path.write_text("")

    return path


@pytest.fixture
def fixed_now() -> datetime:
    return datetime(2010, 10, 20, tzinfo=timezone.utc)


@pytest.fixture
def mock_console() -> Mock:
    return Mock()


@pytest.fixture
def mock_datetime(
    mocker: MockerFixture,
    fixed_now: datetime,
) -> Mock:
    modules_to_patch = (
        "core.terminal.logger.datetime",
        "core.utils.datetime",
    )

    for module in modules_to_patch:
        dt_mock = mocker.patch(module)
        dt_mock.now.return_value = fixed_now

    return dt_mock


@pytest.fixture
def mock_live(
    mocker: MockerFixture,
) -> Mock:
    return mocker.patch(
        "core.terminal.renderers.Live",
        autospec=True,
    )


@pytest.fixture
def mock_log_debug_object(
    mocker: MockerFixture,
) -> Mock:
    mock: Mock = mocker.Mock(
        spec=log_debug_object,
    )

    modules_to_patch = (
        "domain.channel",
    )

    for module in modules_to_patch:
        mocker.patch(
            f"{module}.{log_debug_object.__name__}",
            mock,
        )

    return mock


@pytest.fixture
def mock_logger(
    mocker: MockerFixture,
) -> Mock:
    mock: Mock = mocker.Mock(
        spec=Logger,
    )

    modules_to_patch = (
        "core.decorators.logger",
        "core.terminal.logger.logger",
        "core.utils.logger",
        "domain.channel.logger",
    )

    for module in modules_to_patch:
        mocker.patch(module, mock)

    return mock


@pytest.fixture
def mock_logger_components(
    mocker: MockerFixture,
) -> dict[str, Mock]:
    components = [
        "FileHandler",
        "MicrosecondFormatter",
        "RichHandler",
    ]

    return {
        name: mocker.patch(
            f"core.terminal.logger.{name}",
            autospec=True,
        )
        for name in components
    }


@pytest.fixture
def mock_module_files(
    mocker: MockerFixture,
    tmp_path: Path,
) -> Path:
    modules_to_patch = (
        "core.constants.common.__file__",
        "core.utils.__file__",
    )

    fake_file = _create_file(
        path=tmp_path / "fake_module.py",
        should_create=True,
    )

    for module in modules_to_patch:
        mocker.patch(
            module,
            new=str(fake_file),
        )

    return tmp_path


def pytest_collection_modifyitems(
    config: Config,
    items: list[Item],
) -> None:
    root = Path(__file__).parent.resolve()

    markers_map = {
        "e2e": [
            pytest.mark.e2e,
        ],
        "integration": [
            pytest.mark.integration,
        ],
        "unit": [
            pytest.mark.unit,
        ],
    }

    for item in items:
        path = Path(item.fspath).resolve()

        if not path.is_relative_to(root):
            continue

        markers = [
            mark
            for marker in markers_map
            if marker in path.relative_to(root).parts
            for mark in markers_map[marker]
        ]

        for mark in markers:
            item.add_marker(mark)


@pytest.fixture(autouse=True)
def reset_logger() -> None:
    getLogger(DEFAULT_LOGGER_NAME).handlers.clear()


@pytest.fixture
def tmp_files(
    tmp_path: Path,
) -> list[Path]:
    files_to_create = [
        (
            "missing.log",
            False,
        ),
        (
            "channel.json",
            True,
        ),
        (
            "data.txt",
            True,
        ),
    ]

    return [
        _create_file(
            path=tmp_path / name,
            should_create=make_file,
        )
        for name, make_file in files_to_create
    ]
