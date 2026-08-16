from copy import (
    deepcopy,
)
from dataclasses import (
    dataclass,
)

from core.constants.common import (
    CHANNEL_MIN_ID_DIFF,
    CHANNEL_STATE_AVAILABLE,
    CHANNEL_STATE_UNAVAILABLE,
    DEFAULT_CHANNEL_VALUES,
    DEFAULT_COUNT,
    DEFAULT_CURRENT_ID,
    DEFAULT_LAST_ID,
    DEFAULT_STATE,
    POST_FIRST_ID,
)
from core.constants.messages.error import (
    MESSAGE_ERROR_MULTIPLE_ACTIONS_SPECIFIED,
)
from core.constants.messages.info import (
    MESSAGE_INFO_CHANNEL_DELETE_COMPLETED,
    MESSAGE_INFO_CHANNEL_DELETE_SKIPPED,
    MESSAGE_INFO_CHANNEL_DELETE_STARTED,
    MESSAGE_INFO_CHANNEL_UPDATE_COMPLETED,
    MESSAGE_INFO_CHANNEL_UPDATE_STARTED,
)
from core.constants.messages.warning import (
    MESSAGE_WARNING_NO_CHANNELS_TO_DISPLAY,
)
from core.constants.templates.debug.channel import (
    TEMPLATE_DEBUG_CHANNEL_CHANGES_SKIPPED_NO_CHANGES,
    TEMPLATE_DEBUG_CHANNEL_CHANGES_SKIPPED_TARGETS,
    TEMPLATE_DEBUG_CHANNEL_MISSING_ADD_COMPLETED,
    TEMPLATE_DEBUG_CHANNEL_NORMALIZE_COMPLETED,
    TEMPLATE_DEBUG_CHANNEL_NORMALIZE_NAMES_COMPLETED,
    TEMPLATE_DEBUG_CHANNEL_NORMALIZE_NAMES_DUPLICATE,
    TEMPLATE_DEBUG_CHANNEL_NORMALIZE_NAMES_STARTED,
    TEMPLATE_DEBUG_CHANNEL_NORMALIZE_STARTED,
)
from core.constants.templates.error import (
    TEMPLATE_ERROR_INVALID_OVERRIDE_FIELDS,
)
from core.constants.templates.info.channel import (
    TEMPLATE_INFO_CHANNEL_CHANGES_SKIPPED,
    TEMPLATE_INFO_CHANNEL_CHANGES_TOTAL,
    TEMPLATE_INFO_CHANNELS_STATUS_COMPLETED,
    TEMPLATE_INFO_CHANNELS_STATUS_STARTED,
)
from core.constants.templates.title import (
    TEMPLATE_TITLE_CHANNEL_DELETE,
)
from core.decorators import (
    status,
)
from core.terminal.console import (
    console,
)
from core.terminal.logger import (
    log_channel_changes,
    log_debug_object,
    logger,
)
from core.terminal.renderers import (
    render_channel_status,
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
from domain.predicates import (
    is_channel_pending_update,
    make_predicate,
    should_apply_changes,
    should_delete_channel,
)

__all__ = [
    "ChannelStatus",
    "ChannelUpdateResult",
    "apply_channel_changes",
    "delete_channels",
    "diff_channel_id",
    "display_channel_info",
    "format_channel_status",
    "get_filtered_keys",
    "get_normalized_count",
    "get_normalized_current_id",
    "get_normalized_last_id",
    "get_normalized_state",
    "get_sorted_keys",
    "normalize_channel",
    "normalize_channel_names",
    "normalize_channels",
    "process_channels",
    "sort_channel_names",
    "update_last_id_and_state",
    "update_with_new_channels",
]


@dataclass(slots=True, frozen=True)
class ChannelStatus:
    channel_name: str
    current_id: int
    last_id: int
    diff_id: int


@dataclass(slots=True, frozen=True)
class ChannelUpdateResult:
    channel_name: str
    old_last_id: int
    new_last_id: int
    changed: bool


def apply_channel_changes(
    channels: ChannelsDict,
    *,
    channel_overrides: ChannelInfo | None = None,
    channel_predicate: RecordPredicate | None = None,
    dry_run: bool = True,
    reset_to_defaults: bool = False,
) -> ChannelsDict:
    should_apply = channel_predicate or should_apply_changes
    overrides: ChannelInfo = channel_overrides or {}    # type: ignore[assignment]

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
        logger.debug(  # type: ignore[unreachable]
            msg=TEMPLATE_DEBUG_CHANNEL_CHANGES_SKIPPED_NO_CHANGES.format(
                reset_to_defaults=reset_to_defaults,
                valid_overrides=valid_overrides,
            ),
        )
        return updated_channels

    channel_names_to_update = [
        name
        for name in updated_channels
        if should_apply(updated_channels[name])
    ]

    if dry_run:
        logger.info(
            msg=TEMPLATE_INFO_CHANNEL_CHANGES_SKIPPED.format(
                count=len(channel_names_to_update),
            ),
        )
        logger.debug(
            msg=TEMPLATE_DEBUG_CHANNEL_CHANGES_SKIPPED_TARGETS.format(
                dry_run=dry_run,
                channel_names=channel_names_to_update,
            ),
        )
        return updated_channels

    logger.info(
        msg=TEMPLATE_INFO_CHANNEL_CHANGES_TOTAL.format(
            count=len(channel_names_to_update),
        ),
    )

    base_values = (
        DEFAULT_CHANNEL_VALUES
        if reset_to_defaults else {}    # type: ignore[typeddict-item]
    )

    for name in channel_names_to_update:
        channel_info = updated_channels[name]
        before = channel_info.copy()

        channel_info.update(
            base_values | valid_overrides,
        )

        log_channel_changes(
            name=name,
            before=before,
            after=channel_info,
        )

    return updated_channels


@status(
    start=MESSAGE_INFO_CHANNEL_DELETE_STARTED,
    end=MESSAGE_INFO_CHANNEL_DELETE_COMPLETED,
    tracking=True,
)
def delete_channels(
    channels: ChannelsDict,
    *,
    channel_predicate: RecordPredicate | None = None,
) -> ChannelsDict:
    should_delete = channel_predicate or should_delete_channel

    remaining_channels = deepcopy(
        x=channels,
    )

    for name, info in channels.items():
        if not should_delete(info):
            continue

        log_debug_object(
            obj=info,
            title=TEMPLATE_TITLE_CHANNEL_DELETE.format(
                name=name,
            ),
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


def display_channel_info(
    channels: ChannelsDict,
) -> None:
    channel_names = get_sorted_keys(
        channels=channels,
        apply_filter=True,
    )

    if not channel_names:
        logger.warning(
            msg=MESSAGE_WARNING_NO_CHANNELS_TO_DISPLAY,
        )
        return

    logger.info(
        msg=TEMPLATE_INFO_CHANNELS_STATUS_STARTED.format(
            count=len(channel_names),
        ),
    )

    total_messages = render_channel_status(
        results=[
            format_channel_status(
                channel_name=name,
                channel_info=channels[name],
            )
            for name in channel_names
        ],
        console=console,
    )

    logger.info(
        msg=TEMPLATE_INFO_CHANNELS_STATUS_COMPLETED.format(
            total=len(channels),
            pending=len(channel_names),
            messages=total_messages,
        ),
    )


def format_channel_status(
    channel_name: ChannelName,
    channel_info: ChannelInfo,
) -> ChannelStatus:
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

    return ChannelStatus(
        channel_name=channel_name,
        current_id=current_id,
        last_id=last_id,
        diff_id=diff,
    )


def get_filtered_keys(
    channels: ChannelsDict,
) -> ChannelNames:
    return [
        name
        for name, info in channels.items()
        if is_channel_pending_update(
            channel_info=info,
        )
    ]


def get_normalized_count(
    channel_info: ChannelInfo,
) -> int:
    count = channel_info.get(
        "count",
        DEFAULT_COUNT,
    )

    return max(
        count,
        DEFAULT_COUNT,
    )


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

    if last_id == DEFAULT_LAST_ID:
        return max(
            current_id,
            DEFAULT_CURRENT_ID,
        )

    if current_id < DEFAULT_CURRENT_ID:
        current_id += last_id

    return min(
        max(
            current_id,
            DEFAULT_CURRENT_ID,
        ),
        last_id,
    )


def get_normalized_last_id(
    channel_info: ChannelInfo,
) -> PostID:
    last_id = channel_info.get(
        "last_id",
        DEFAULT_LAST_ID,
    )

    if last_id < POST_FIRST_ID:
        return DEFAULT_LAST_ID

    return last_id


def get_normalized_state(
    channel_info: ChannelInfo,
) -> int:
    last_id = channel_info.get(
        "last_id",
        DEFAULT_LAST_ID,
    )
    state = channel_info.get(
        "state",
        DEFAULT_STATE,
    )

    if last_id != DEFAULT_LAST_ID:
        return CHANNEL_STATE_AVAILABLE

    return min(
        state,
        DEFAULT_STATE,
    )


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


def normalize_channel(
    channel_info: ChannelInfo,
) -> ChannelInfo:
    result: ChannelInfo = {  # type: ignore[assignment]
        key: channel_info.get(key, default)
        for key, default in DEFAULT_CHANNEL_VALUES.items()
    }

    field_normalizers = {
        "count": get_normalized_count,
        "last_id": get_normalized_last_id,
        "current_id": get_normalized_current_id,
        "state": get_normalized_state,
    }

    for field, normalizer in field_normalizers.items():
        result[field] = normalizer(  # type: ignore[literal-required]
            channel_info=result,
        )

    return result


def normalize_channel_names(
    channels: ChannelsDict,
) -> ChannelsDict:
    normalized_channels: ChannelsDict = {}

    logger.debug(
        msg=TEMPLATE_DEBUG_CHANNEL_NORMALIZE_NAMES_STARTED.format(
            channels_count=len(channels),
        ),
    )

    for name, info in channels.items():
        normalized_name = str(name).lower()

        if normalized_name in normalized_channels:
            logger.debug(
                msg=TEMPLATE_DEBUG_CHANNEL_NORMALIZE_NAMES_DUPLICATE.format(
                    channel_name=name,
                    normalized_channel_name=normalized_name,
                ),
            )
            continue

        normalized_channels[normalized_name] = info

    logger.debug(
        msg=TEMPLATE_DEBUG_CHANNEL_NORMALIZE_NAMES_COMPLETED.format(
            channels_count=len(channels),
            normalized_channels_count=len(normalized_channels),
        ),
    )

    return normalized_channels


def normalize_channels(
    channels: ChannelsDict,
) -> ChannelsDict:
    logger.debug(
        msg=TEMPLATE_DEBUG_CHANNEL_NORMALIZE_STARTED.format(
            channels_count=len(channels),
        ),
    )

    channels_with_normalized_names = normalize_channel_names(
        channels=channels,
    )

    normalized_channels: ChannelsDict = {}

    for name, info in channels_with_normalized_names.items():
        normalized_info = normalize_channel(
            channel_info=info,
        )

        log_channel_changes(
            name=name,
            before=info,
            after=normalized_info,
        )

        normalized_channels[name] = normalized_info

    logger.debug(
        msg=TEMPLATE_DEBUG_CHANNEL_NORMALIZE_COMPLETED.format(
            channels_count=len(normalized_channels),
        ),
    )

    return normalized_channels


def process_channels(
    channels: ChannelsDict,
    args: ArgsNamespace,
) -> ChannelsDict:
    channel_overrides: ChannelInfo = {  # type: ignore[assignment]
        key: value
        for key in DEFAULT_CHANNEL_VALUES
        if (value := getattr(args, f"set_{key}", None)) is not None
    }
    channel_predicate = make_predicate(
        condition=args.channel_filter,
    )

    action_count = sum((
        args.delete_channels,
        bool(channel_overrides) or args.reset_all,
    ))

    if action_count > 1:
        logger.error(
            msg=MESSAGE_ERROR_MULTIPLE_ACTIONS_SPECIFIED,
        )
        return channels

    if args.delete_channels:
        channels = delete_channels(
            channels=channels,
            channel_predicate=channel_predicate,
        )
    else:
        logger.info(
            msg=MESSAGE_INFO_CHANNEL_DELETE_SKIPPED,
        )

    if channel_overrides or args.reset_all:  # type: ignore[unreachable]
        channels = apply_channel_changes(
            channels=channels,
            channel_overrides=channel_overrides,
            channel_predicate=channel_predicate,
            dry_run=args.dry_run,
            reset_to_defaults=args.reset_all,
        )

    return channels


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
    *,
    last_post_id: PostID,
) -> ChannelUpdateResult:
    last_id = channel_info.get(
        "last_id",
        DEFAULT_LAST_ID,
    )
    state = channel_info.get(
        "state",
        DEFAULT_STATE,
    )
    changed = last_id != last_post_id

    if changed:
        channel_info["last_id"] = last_post_id

    if last_post_id != DEFAULT_LAST_ID:
        channel_info["state"] = CHANNEL_STATE_AVAILABLE
    elif changed:
        channel_info["state"] = DEFAULT_STATE
    else:
        channel_info["state"] = min(
            state - 1,
            CHANNEL_STATE_UNAVAILABLE,
        )

    return ChannelUpdateResult(
        channel_name=channel_name,
        old_last_id=last_id,
        new_last_id=last_post_id,
        changed=changed,
    )


@status(
    start=MESSAGE_INFO_CHANNEL_UPDATE_STARTED,
    end=MESSAGE_INFO_CHANNEL_UPDATE_COMPLETED,
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
                msg=TEMPLATE_DEBUG_CHANNEL_MISSING_ADD_COMPLETED.format(
                    name=name,
                ),
            )

    return updated_channels
