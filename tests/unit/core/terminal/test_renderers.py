from unittest.mock import (
    Mock,
)

from core.terminal.renderers import (
    render_channel_status,
    render_channel_update,
    render_config_extract,
)
from domain.channel import (
    ChannelStatus,
    ChannelUpdateResult,
)
from domain.config import (
    ConfigExtractionResult,
)


def test_render_channel_status_returns_total_diff(
    mock_console: Mock,
) -> None:
    results = [
        ChannelStatus(
            channel_name="channel_1",
            current_id=100,
            last_id=1000,
            diff_id=900,
        ),
        ChannelStatus(
            channel_name="channel_2",
            current_id=200,
            last_id=200,
            diff_id=0,
        ),
        ChannelStatus(
            channel_name="channel_3",
            current_id=400,
            last_id=500,
            diff_id=100,
        ),
    ]

    total_diff = render_channel_status(
        results=results,
        console=mock_console,
    )

    assert total_diff == 1000
    mock_console.print.assert_called_once()


def test_render_channel_update_returns_one_when_changed(
    mock_live: Mock,
) -> None:
    with render_channel_update() as add_update:
        result = add_update(
            ChannelUpdateResult(
                channel_name="channel",
                old_last_id=1111,
                new_last_id=2222,
                changed=True,
            ),
        )

    assert result == 1


def test_render_channel_update_returns_zero_when_not_changed(
    mock_live: Mock,
) -> None:
    with render_channel_update() as add_update:
        result = add_update(
            ChannelUpdateResult(
                channel_name="channel",
                old_last_id=1111,
                new_last_id=1111,
                changed=False,
            ),
        )

    assert result == 0


def test_render_config_extract_prints(
    mock_console: Mock,
) -> None:
    results = [
        ConfigExtractionResult(
            channel_name="channel",
            total_found=10,
            new_found=5,
        ),
    ]

    render_config_extract(
        results=results,
        console=mock_console,
    )

    mock_console.print.assert_called_once()
