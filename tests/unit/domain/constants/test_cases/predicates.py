import pytest

from tests.unit.domain.constants.examples.predicates import (
    IS_CHANNEL_AVAILABLE_EXAMPLES,
    IS_CHANNEL_FULLY_SCANNED_EXAMPLES,
    IS_NEW_CHANNEL_EXAMPLES,
    MAKE_PREDICATE_EXAMPLES,
    SHOULD_DELETE_CHANNEL_EXAMPLES,
    SHOULD_SET_CURRENT_ID_EXAMPLES,
    SHOULD_UPDATE_CHANNEL_EXAMPLES,
)

IS_CHANNEL_AVAILABLE_ARGS = (
    "channel_info",
    "expected",
)
IS_CHANNEL_AVAILABLE_CASES = tuple(
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

IS_CHANNEL_FULLY_SCANNED_ARGS = (
    "channel_info",
    "expected",
)
IS_CHANNEL_FULLY_SCANNED_CASES = tuple(
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

IS_NEW_CHANNEL_ARGS = (
    "channel_info",
    "expected",
)
IS_NEW_CHANNEL_CASES = tuple(
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

MAKE_PREDICATE_ARGS = (
    "condition",
    "config",
    "expected",
)
MAKE_PREDICATE_CASES = tuple(
    pytest.param(
        condition,
        config,
        expected,
        id=case_id,
    )
    for (
        condition,
        config,
        expected,
        case_id,
    ) in MAKE_PREDICATE_EXAMPLES
)

SHOULD_DELETE_CHANNEL_ARGS = (
    "channel_info",
    "expected",
)
SHOULD_DELETE_CHANNEL_CASES = tuple(
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

SHOULD_SET_CURRENT_ID_ARGS = (
    "channel_info",
    "expected",
)
SHOULD_SET_CURRENT_ID_CASES = tuple(
    pytest.param(
        channel_info,
        expected,
        id=case_id,
    )
    for (
        channel_info,
        expected,
        case_id,
    ) in SHOULD_SET_CURRENT_ID_EXAMPLES
)

SHOULD_UPDATE_CHANNEL_ARGS = (
    "channel_info",
    "expected",
)
SHOULD_UPDATE_CHANNEL_CASES = tuple(
    pytest.param(
        channel_info,
        expected,
        id=case_id,
    )
    for (
        channel_info,
        expected,
        case_id,
    ) in SHOULD_UPDATE_CHANNEL_EXAMPLES
)
