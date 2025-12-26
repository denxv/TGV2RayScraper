from datetime import (
    datetime,
    timedelta,
    timezone,
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
from freezegun import (
    freeze_time,
)
from pytest_mock import (
    MockerFixture,
)

from core.logger import (
    Logger,
    log_debug_object,
)
from core.typing import (
    Iterator,
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
def frozen_datetime_local_tz() -> Iterator[datetime]:
    local_tz = datetime.now().astimezone().tzinfo

    fixed_dt = datetime(
        year=2020,
        month=11,
        day=11,
        hour=12,
        minute=12,
        second=12,
        tzinfo=local_tz)

    with freeze_time(fixed_dt):
        yield datetime.now().astimezone()


@pytest.fixture(
    params=list(
        range(-9, 10, 3),
    ),
    ids=[
        f"UTC{offset:+d}"
        for offset in range(-9, 10, 3)
    ],
)
def frozen_datetime_offset(
    request: pytest.FixtureRequest,
    frozen_datetime_local_tz: datetime,
) -> datetime:
    return datetime.now(
        tz=timezone(
            timedelta(
                hours=request.param,
            ),
        ),
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
        "core.logger.logger",
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
        "StreamHandler",
    ]

    return {
        name: mocker.patch(
            f"core.logger.{name}",
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
