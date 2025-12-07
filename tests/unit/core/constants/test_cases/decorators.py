import pytest

from tests.unit.core.constants.examples.decorators import (
    STATUS_TRACKING_COMBINED_EXAMPLES,
)

STATUS_TRACKING_COMBINED_ARGS = (
    "args",
    "kwargs",
    "output_dict",
    "tracking",
    "expect_diff_log",
)
STATUS_TRACKING_COMBINED_CASES = tuple(
    pytest.param(
        args,
        kwargs,
        output_dict,
        tracking,
        expect_diff_log,
        id=case_id,
    )
    for (
        args,
        kwargs,
        output_dict,
        tracking,
        expect_diff_log,
        case_id,
    ) in STATUS_TRACKING_COMBINED_EXAMPLES
)
