from functools import (
    wraps,
)

from core.constants.templates import (
    TEMPLATE_CHANNEL_COUNT_DIFFERENCE,
)
from core.logger import (
    logger,
)
from core.typing import (
    Callable,
    P,
    T,
)

__all__ = [
    "status",
]


def status(
    start: str,
    end: str = "",
    *,
    tracking: bool = False,
) -> Callable[[Callable[P, T]], Callable[P, T]]:

    def decorator(
        target_func: Callable[P, T],
    ) -> Callable[P, T]:

        @wraps(target_func)
        def wrapper(
            *args: P.args,
            **kwargs: P.kwargs,
        ) -> T:
            logger.info(
                msg=start,
            )

            first_value: object = next(
                iter(kwargs.values()),
                None,
            )
            if args:
                first_value = args[0]

            old_size: int | None = None
            if (
                tracking
                and isinstance(first_value, dict)
            ):
                old_size = len(first_value)

            result: T = target_func(
                *args,
                **kwargs,
            )

            if (
                old_size is not None
                and isinstance(result, dict)
            ):
                new_size = len(result)
                logger.info(
                    msg=TEMPLATE_CHANNEL_COUNT_DIFFERENCE.format(
                        old_size=old_size,
                        new_size=new_size,
                        diff=new_size - old_size,
                    ),
                )

            if end:
                logger.info(
                    msg=end,
                )

            return result

        return wrapper

    return decorator
