from copy import (
    deepcopy,
)

from core.constants.common import (
    CHANNEL_MIN_ID_DIFF,
    CHANNEL_STATE_AVAILABLE,
    CHANNEL_STATE_UNAVAILABLE,
    DEFAULT_CHANNEL_VALUES,
    DEFAULT_CURRENT_ID,
    DEFAULT_LAST_ID,
    DEFAULT_STATE,
    MESSAGE_OFFSET_DEFAULT,
)
from core.constants.messages import (
    MESSAGE_CHANNEL_DELETE_COMPLETED,
    MESSAGE_CHANNEL_DELETE_SKIPPED,
    MESSAGE_CHANNEL_DELETE_STARTED,
    MESSAGE_CHANNEL_SHOW_INFO,
    MESSAGE_CHANNEL_UPDATE_COMPLETED,
    MESSAGE_CHANNEL_UPDATE_STARTED,
)
from core.constants.templates import (
    TEMPLATE_CHANNEL_ASSIGNMENT_APPLIED,
    TEMPLATE_CHANNEL_ASSIGNMENT_OFFSET_APPLIED,
    TEMPLATE_CHANNEL_ASSIGNMENT_OFFSET_SKIPPED,
    TEMPLATE_CHANNEL_ASSIGNMENT_SKIPPED,
    TEMPLATE_CHANNEL_LEFT_TO_CHECK,
    TEMPLATE_CHANNEL_LOG_STATUS,
    TEMPLATE_CHANNEL_LOG_UPDATE,
    TEMPLATE_CHANNEL_MISSING_ADD_COMPLETED,
    TEMPLATE_CHANNEL_RESET_SKIPPED,
    TEMPLATE_CHANNEL_RESET_SKIPPED_NO_CHANGES,
    TEMPLATE_CHANNEL_RESET_TOTAL,
    TEMPLATE_CHANNEL_TOTAL_AVAILABLE,
    TEMPLATE_CHANNEL_TOTAL_MESSAGES,
    TEMPLATE_ERROR_INVALID_OFFSET,
    TEMPLATE_ERROR_INVALID_OVERRIDE_FIELDS,
    TEMPLATE_FORMAT_CHANNEL_CHANGE,
    TEMPLATE_FORMAT_STRING_QUOTED_NAME,
    TEMPLATE_TITLE_CHANNEL_DELETE,
    TEMPLATE_TITLE_CHANNEL_INFO,
    TEMPLATE_TITLE_CHANNEL_RESET,
)
from core.decorators import (
    status,
)
from core.logger import (
    log_debug_object,
    logger,
)
from core.typing import (
    ArgsNamespace,
    ChannelInfo,
    ChannelName,
    ChannelNames,
    ChannelsDict,
    PostID,
    RecordPredicate,
)
from core.utils import (
    repeat_char_line,
)
from domain.predicates import (
    is_channel_available,
    is_channel_fully_scanned,
    make_predicate,
    should_delete_channel,
    should_set_current_id,
    should_update_channel,
)

__all__ = [
    "assign_current_id_to_channels",
    "delete_channels",
    "diff_channel_id",
    "format_channel_status",
    "get_filtered_keys",
    "get_normalized_current_id",
    "get_sorted_keys",
    "normalize_channel_names",
    "print_channel_info",
    "process_channels",
    "reset_channels",
    "sort_channel_names",
    "update_last_id_and_state",
    "update_with_new_channels",
]


def assign_current_id_to_channels(
    channels: ChannelsDict,
    message_offset: int = MESSAGE_OFFSET_DEFAULT,
    *,
    dry_run: bool = False,
) -> ChannelsDict:
    updated_channels = deepcopy(
        x=channels,
    )

    if (
        not isinstance(message_offset, int)
        or message_offset <= 0
    ):
        logger.warning(
            msg=TEMPLATE_ERROR_INVALID_OFFSET.format(
                offset=message_offset,
            ),
        )
        return updated_channels

    channel_names_for_update = [
        name
        for name in updated_channels
        if should_set_current_id(
            channel_info=updated_channels[name],
        )
    ]

    for name in channel_names_for_update:
        diff = diff_channel_id(
            channel_info=updated_channels[name],
        )

        if diff <= message_offset:  # pragma: no cover
            continue

        _message = TEMPLATE_CHANNEL_ASSIGNMENT_OFFSET_SKIPPED.format(
            name=TEMPLATE_FORMAT_STRING_QUOTED_NAME.format(
                name=name,
            ),
            diff=diff,
            offset=message_offset,
        )

        if dry_run:
            log_debug_object(
                title=TEMPLATE_TITLE_CHANNEL_INFO.format(
                    name=name,
                ),
                obj=updated_channels[name],
            )
            logger.warning(
                msg=_message,
            )
        else:
            logger.debug(
                msg=TEMPLATE_CHANNEL_ASSIGNMENT_OFFSET_APPLIED.format(
                    message=_message,
                ),
            )

    if dry_run:
        logger.info(
            msg=TEMPLATE_CHANNEL_ASSIGNMENT_SKIPPED.format(
                count=len(channel_names_for_update),
            ),
        )
        return updated_channels

    for name in channel_names_for_update:
        current_info: ChannelInfo = updated_channels.get(name, {})

        current_info["current_id"] = get_normalized_current_id(
            channel_info={
                **current_info,
                "current_id": -message_offset,
            },
        )

        logger.info(
            msg=TEMPLATE_CHANNEL_ASSIGNMENT_APPLIED.format(
                name=TEMPLATE_FORMAT_STRING_QUOTED_NAME.format(
                    name=name,
                ),
                offset=-message_offset,
            ),
        )

    return updated_channels


@status(
    start=MESSAGE_CHANNEL_DELETE_STARTED,
    end=MESSAGE_CHANNEL_DELETE_COMPLETED,
    tracking=True,
)
def delete_channels(
    channels: ChannelsDict,
) -> ChannelsDict:
    remaining_channels = deepcopy(
        x=channels,
    )

    for name, info in channels.items():
        normalized_info: ChannelInfo = {
            **info,
            "current_id": get_normalized_current_id(
                channel_info=info,
            ),
        }

        if should_delete_channel(
            channel_info=normalized_info,
        ):
            log_debug_object(
                title=TEMPLATE_TITLE_CHANNEL_DELETE.format(
                    name=name,
                ),
                obj=info,
            )

            remaining_channels.pop(name, None)

    return remaining_channels


def diff_channel_id(
    channel_info: ChannelInfo,
) -> int:
    current_id = get_normalized_current_id(
        channel_info=channel_info,
    )
    last_id = channel_info.get(
        "last_id",
        DEFAULT_LAST_ID,
    )

    return max(
        CHANNEL_MIN_ID_DIFF,
        last_id - current_id,
    )


def format_channel_status(
    channel_name: ChannelName,
    channel_info: ChannelInfo,
) -> tuple[int, str]:
    diff = diff_channel_id(
        channel_info=channel_info,
    )

    current_id = get_normalized_current_id(
        channel_info=channel_info,
    )
    last_id = channel_info.get(
        "last_id",
        DEFAULT_LAST_ID,
    )

    return (
        diff,
        TEMPLATE_CHANNEL_LOG_STATUS.format(
            name=channel_name,
            current_id=current_id,
            last_id=last_id,
            diff=diff,
        ),
    )


def get_filtered_keys(
    channels: ChannelsDict,
) -> ChannelNames:
    filtered_keys = []

    for name, info in channels.items():
        normalized_info: ChannelInfo = {
            **info,
            "current_id": get_normalized_current_id(
                channel_info=info,
            ),
        }

        if should_update_channel(
            channel_info=normalized_info,
        ):
            filtered_keys.append(name)

    return filtered_keys


def get_normalized_current_id(
    channel_info: ChannelInfo,
) -> PostID:
    current_id = channel_info.get(
        "current_id",
        DEFAULT_CURRENT_ID,
    )
    last_id = channel_info.get(
        "last_id",
        DEFAULT_LAST_ID,
    )

    if not is_channel_available(
        channel_info=channel_info,
    ):
        return DEFAULT_CURRENT_ID

    if current_id <= 0:
        return max(
            last_id + current_id,
            DEFAULT_CURRENT_ID,
        )

    if is_channel_fully_scanned(
        channel_info=channel_info,
    ):
        return last_id

    return current_id


def get_sorted_keys(
    channels: ChannelsDict,
    *,
    apply_filter: bool = False,
    reverse: bool = False,
) -> ChannelNames:
    channel_names = list(channels)

    if apply_filter:
        channel_names = get_filtered_keys(
            channels=channels,
        )

    return sorted(
        channel_names,
        key=lambda name: (
            diff_channel_id(
                channel_info=channels[name],
            ),
            name,
        ),
        reverse=reverse,
    )


def normalize_channel_names(
    channels: ChannelsDict,
) -> ChannelsDict:
    normalized: ChannelsDict = {}

    for name, info in channels.items():
        normalized.setdefault(
            str(name).lower(),
            info,
        )

    return normalized


def print_channel_info(channels: ChannelsDict) -> None:
    separator_line = repeat_char_line(
        char="-",
    )
    logger.info(
        msg=separator_line,
    )
    logger.info(
        msg=MESSAGE_CHANNEL_SHOW_INFO,
    )

    total_channels_post = 0
    channel_names = get_sorted_keys(
        channels=channels,
        apply_filter=True,
    )

    for name in channel_names:
        diff, status_line = format_channel_status(
            channel_name=name,
            channel_info=channels[name],
        )
        total_channels_post += diff

        logger.info(
            msg=status_line,
        )

    logger.info(
        msg=TEMPLATE_CHANNEL_TOTAL_AVAILABLE.format(
            count=len(channels),
        ),
    )
    logger.info(
        msg=TEMPLATE_CHANNEL_LEFT_TO_CHECK.format(
            count=len(channel_names),
        ),
    )
    logger.info(
        msg=TEMPLATE_CHANNEL_TOTAL_MESSAGES.format(
            count=total_channels_post,
        ),
    )
    logger.info(
        msg=separator_line,
    )


def process_channels(
    channels: ChannelsDict,
    args: ArgsNamespace,
) -> ChannelsDict:
    if args.delete_channels:
        channels = delete_channels(
            channels=channels,
        )
    else:
        logger.info(
            msg=MESSAGE_CHANNEL_DELETE_SKIPPED,
        )

    if args.message_offset:
        channels = assign_current_id_to_channels(
            channels=channels,
            message_offset=args.message_offset,
            dry_run=args.dry_run,
        )

    channel_overrides: ChannelInfo = {  # type: ignore[assignment]
        key: value
        for key in DEFAULT_CHANNEL_VALUES
        if (value := getattr(args, f"reset_{key}", None)) is not None
    }

    if channel_overrides or args.reset_all:
        channels = reset_channels(
            channels=channels,
            channel_overrides=channel_overrides,
            channel_predicate=make_predicate(
                condition=args.channel_filter,
            ),
            dry_run=args.dry_run,
            reset_to_defaults=args.reset_all,
        )

    return channels


def reset_channels(
    channels: ChannelsDict,
    channel_overrides: ChannelInfo | None = None,
    channel_predicate: RecordPredicate | None = None,
    *,
    dry_run: bool = True,
    reset_to_defaults: bool = False,
) -> ChannelsDict:
    overrides: ChannelInfo = channel_overrides or {}

    if invalid_fields := set(overrides) - set(DEFAULT_CHANNEL_VALUES):
        raise ValueError(
            TEMPLATE_ERROR_INVALID_OVERRIDE_FIELDS.format(
                fields=invalid_fields,
            ),
        )

    updated_channels = deepcopy(
        x=channels,
    )
    valid_overrides: ChannelInfo = {  # type: ignore[assignment]
        key: value
        for key, value in overrides.items()
        if value is not None
    }

    if not reset_to_defaults and not valid_overrides:
        logger.debug(
            msg=TEMPLATE_CHANNEL_RESET_SKIPPED_NO_CHANGES.format(
                reset_to_defaults=reset_to_defaults,
                valid_overrides=valid_overrides,
            ),
        )
        return updated_channels

    channel_selector = (
        channel_predicate
        or should_set_current_id
    )
    channel_names_to_reset = [
        name
        for name in updated_channels
        if channel_selector(
            updated_channels[name],
        )
    ]

    if dry_run:
        logger.info(
            msg=TEMPLATE_CHANNEL_RESET_SKIPPED.format(
                count=len(channel_names_to_reset),
            ),
        )
        return updated_channels

    logger.info(
        msg=TEMPLATE_CHANNEL_RESET_TOTAL.format(
            count=len(channel_names_to_reset),
        ),
    )

    reset_base = (
        DEFAULT_CHANNEL_VALUES
        if reset_to_defaults else {}
    )

    for name in channel_names_to_reset:
        channel_info = updated_channels[name]
        before = channel_info.copy()

        channel_info.update(
            reset_base | valid_overrides,
        )

        log_debug_object(
            title=TEMPLATE_TITLE_CHANNEL_RESET.format(
                name=name,
            ),
            obj={
                key: TEMPLATE_FORMAT_CHANNEL_CHANGE.format(
                    before=before.get(key),
                    after=channel_info[key],  # type: ignore[literal-required]
                )
                for key in channel_info
                if before.get(key) != channel_info[key]  # type: ignore[literal-required]
            },
        )

    return updated_channels


def sort_channel_names(
    channel_names: ChannelNames,
    *,
    ignore_case: bool = True,
    reverse: bool = False,
) -> ChannelNames:
    return sorted(
        channel_names,
        key=(
            str.lower if ignore_case else None
        ),
        reverse=reverse,
    )


def update_last_id_and_state(
    channel_name: ChannelName,
    channel_info: ChannelInfo,
    last_post_id: PostID,
) -> None:
    last_id = channel_info.get(
        "last_id",
        DEFAULT_LAST_ID,
    )
    state = channel_info.get(
        "state",
        DEFAULT_STATE,
    )

    if last_id != last_post_id:
        logger.info(
            msg=TEMPLATE_CHANNEL_LOG_UPDATE.format(
                name=channel_name,
                last_id=last_id,
                last_post_id=last_post_id,
            ),
        )
        channel_info["last_id"] = last_post_id

    if last_post_id != DEFAULT_LAST_ID:
        channel_info["state"] = CHANNEL_STATE_AVAILABLE
    elif last_id != last_post_id:
        channel_info["state"] = DEFAULT_STATE
    else:
        channel_info["state"] = min(
            state - 1,
            CHANNEL_STATE_UNAVAILABLE,
        )


@status(
    start=MESSAGE_CHANNEL_UPDATE_STARTED,
    end=MESSAGE_CHANNEL_UPDATE_COMPLETED,
    tracking=True,
)
def update_with_new_channels(
    current_channels: ChannelsDict,
    channel_names: ChannelNames,
) -> ChannelsDict:
    updated_channels = deepcopy(
        x=current_channels,
    )

    for name in sort_channel_names(
        channel_names=channel_names,
    ):
        updated_channels.setdefault(
            name,
            DEFAULT_CHANNEL_VALUES.copy(),
        )

        if name not in current_channels:
            logger.debug(
                msg=TEMPLATE_CHANNEL_MISSING_ADD_COMPLETED.format(
                    name=name,
                ),
            )

    return updated_channels
