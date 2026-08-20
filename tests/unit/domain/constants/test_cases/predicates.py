import pytest

from tests.unit.domain.constants.examples.predicates import (
    HAS_MULTIPLE_CHANNEL_ACTIONS_EXAMPLES,
    IS_CHANNEL_AVAILABLE_EXAMPLES,
    IS_CHANNEL_FULLY_SCANNED_EXAMPLES,
    IS_CHANNEL_PENDING_UPDATE_EXAMPLES,
    IS_NEW_CHANNEL_EXAMPLES,
    MAKE_PREDICATE_EXAMPLES,
    SHOULD_APPLY_CHANGES_EXAMPLES,
    SHOULD_DELETE_CHANNEL_EXAMPLES,
)

__all__ = [
    "HAS_MULTIPLE_CHANNEL_ACTIONS_ARGS",
    "HAS_MULTIPLE_CHANNEL_ACTIONS_CASES",
    "IS_CHANNEL_AVAILABLE_ARGS",
    "IS_CHANNEL_AVAILABLE_CASES",
    "IS_CHANNEL_FULLY_SCANNED_ARGS",
    "IS_CHANNEL_FULLY_SCANNED_CASES",
    "IS_CHANNEL_PENDING_UPDATE_ARGS",
    "IS_CHANNEL_PENDING_UPDATE_CASES",
    "IS_NEW_CHANNEL_ARGS",
    "IS_NEW_CHANNEL_CASES",
    "MAKE_PREDICATE_ARGS",
    "MAKE_PREDICATE_CASES",
    "SHOULD_APPLY_CHANGES_ARGS",
    "SHOULD_APPLY_CHANGES_CASES",
    "SHOULD_DELETE_CHANNEL_ARGS",
    "SHOULD_DELETE_CHANNEL_CASES",
]

HAS_MULTIPLE_CHANNEL_ACTIONS_ARGS: tuple[
    str,
    ...,
] = (
    "has_overrides",
    "reset_to_defaults",
    "should_delete",
    "expected",
)
HAS_MULTIPLE_CHANNEL_ACTIONS_CASES: tuple[
    object,
    ...,
] = tuple(
    pytest.param(
        has_overrides,
        reset_to_defaults,
        should_delete,
        expected,
        id=case_id,
    )
    for (
        has_overrides,
        reset_to_defaults,
        should_delete,
        expected,
        case_id,
    ) in HAS_MULTIPLE_CHANNEL_ACTIONS_EXAMPLES
)

IS_CHANNEL_AVAILABLE_ARGS: tuple[
    str,
    ...,
] = (
    "channel_info",
    "expected",
)
IS_CHANNEL_AVAILABLE_CASES: tuple[
    object,
    ...,
] = tuple(
    pytest.param(
        channel_info,
        expected,
        id=case_id,
    )
    for (
        channel_info,
        expected,
        case_id,
    ) in IS_CHANNEL_AVAILABLE_EXAMPLES
)

IS_CHANNEL_FULLY_SCANNED_ARGS: tuple[
    str,
    ...,
] = (
    "channel_info",
    "expected",
)
IS_CHANNEL_FULLY_SCANNED_CASES: tuple[
    object,
    ...,
] = tuple(
    pytest.param(
        channel_info,
        expected,
        id=case_id,
    )
    for (
        channel_info,
        expected,
        case_id,
    ) in IS_CHANNEL_FULLY_SCANNED_EXAMPLES
)

IS_CHANNEL_PENDING_UPDATE_ARGS: tuple[
    str,
    ...,
] = (
    "channel_info",
    "expected",
)
IS_CHANNEL_PENDING_UPDATE_CASES: tuple[
    object,
    ...,
] = tuple(
    pytest.param(
        channel_info,
        expected,
        id=case_id,
    )
    for (
        channel_info,
        expected,
        case_id,
    ) in IS_CHANNEL_PENDING_UPDATE_EXAMPLES
)

IS_NEW_CHANNEL_ARGS: tuple[
    str,
    ...,
] = (
    "channel_info",
    "expected",
)
IS_NEW_CHANNEL_CASES: tuple[
    object,
    ...,
] = tuple(
    pytest.param(
        channel_info,
        expected,
        id=case_id,
    )
    for (
        channel_info,
        expected,
        case_id,
    ) in IS_NEW_CHANNEL_EXAMPLES
)

MAKE_PREDICATE_ARGS: tuple[
    str,
    ...,
] = (
    "condition",
    "record",
    "expected",
)
MAKE_PREDICATE_CASES: tuple[
    object,
    ...,
] = tuple(
    pytest.param(
        condition,
        record,
        expected,
        id=case_id,
    )
    for (
        condition,
        record,
        expected,
        case_id,
    ) in MAKE_PREDICATE_EXAMPLES
)

SHOULD_APPLY_CHANGES_ARGS: tuple[
    str,
    ...,
] = (
    "channel_info",
    "expected",
)
SHOULD_APPLY_CHANGES_CASES: tuple[
    object,
    ...,
] = tuple(
    pytest.param(
        channel_info,
        expected,
        id=case_id,
    )
    for (
        channel_info,
        expected,
        case_id,
    ) in SHOULD_APPLY_CHANGES_EXAMPLES
)

SHOULD_DELETE_CHANNEL_ARGS: tuple[
    str,
    ...,
] = (
    "channel_info",
    "expected",
)
SHOULD_DELETE_CHANNEL_CASES: tuple[
    object,
    ...,
] = tuple(
    pytest.param(
        channel_info,
        expected,
        id=case_id,
    )
    for (
        channel_info,
        expected,
        case_id,
    ) in SHOULD_DELETE_CHANNEL_EXAMPLES
)
