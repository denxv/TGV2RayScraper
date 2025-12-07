from unittest.mock import (
    Mock,
)

import pytest

from core.decorators import (
    status,
)
from tests.unit.core.constants.common import (
    TEMPLATE_CHANNEL_COUNT_DIFFERENCE,
)
from tests.unit.core.constants.test_cases.decorators import (
    STATUS_TRACKING_COMBINED_ARGS,
    STATUS_TRACKING_COMBINED_CASES,
)


def test_status_logs_start_and_end(
    mock_logger: Mock,
) -> None:

    @status(
        start="Begin",
        end="End",
    )
    def get_ok() -> str:
        return "ok"

    result = get_ok()

    mock_logger.info.assert_any_call(
        msg="Begin",
    )
    mock_logger.info.assert_any_call(
        msg="End",
    )

    assert result == "ok"
    assert mock_logger.info.call_count == 2


def test_status_logs_start_only(
    mock_logger: Mock,
) -> None:

    @status(
        start="OnlyStart",
    )
    def do_nothing() -> None:
        pass

    do_nothing()

    mock_logger.info.assert_called_once_with(
        msg="OnlyStart",
    )


def test_status_preserves_function_metadata(
    mock_logger: Mock,
) -> None:

    @status(
        start="Meta",
        tracking=True,
    )
    def int_to_str(
        x: int,
    ) -> str:
        """Converts int to string."""
        return str(x)

    result = int_to_str(
        x=10,
    )

    assert result == "10"
    assert int_to_str.__name__ == "int_to_str"
    assert int_to_str.__doc__ == "Converts int to string."


@pytest.mark.parametrize(
    STATUS_TRACKING_COMBINED_ARGS,
    STATUS_TRACKING_COMBINED_CASES,
)
def test_status_tracking_combined(
    mock_logger: Mock,
    args: tuple[dict[str, int]],
    kwargs: dict[str, object],
    output_dict: dict[str, int],
    *,
    tracking: bool,
    expect_diff_log: bool,
) -> None:

    @status(
        start="Process",
        tracking=tracking,
    )
    def modify(
        *args: tuple[dict[str, int]],
        **kwargs: dict[str, object],
    ) -> dict[str, int]:
        return output_dict

    modify(
        *args,
        **kwargs,
    )

    expected_calls = 2 if expect_diff_log else 1

    mock_logger.info.assert_any_call(
        msg="Process",
    )

    assert mock_logger.info.call_count == expected_calls

    if expect_diff_log:
        old_size = len(
            kwargs.get("data", {}) if kwargs else args[0],
        )

        mock_logger.info.assert_any_call(
            msg=TEMPLATE_CHANNEL_COUNT_DIFFERENCE.format(
                old_size=old_size,
                new_size=len(output_dict),
                diff=len(output_dict) - old_size,
            ),
        )
