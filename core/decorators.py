from functools import wraps

from core.typing import (
    Callable,
    Optional,
    P,
    T,
)
from core.logger import logger


def status(
    start: str,
    end: str = "",
    tracking: bool = False,
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    def decorator(target_func: Callable[P, T]) -> Callable[P, T]:
        @wraps(target_func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            logger.info(start)
            first_value: object = args[0] if args else next(iter(kwargs.values()), None)

            old_size: Optional[int] = None
            if tracking and isinstance(first_value, dict):
                old_size = len(first_value)

            result: T = target_func(*args, **kwargs)

            if old_size is not None and isinstance(result, dict):
                new_size = len(result)
                diff = new_size - old_size
                logger.info(f"Old count: {old_size} | New count: {new_size} | ({diff:+})")

            if end:
                logger.info(end)

            return result
        return wrapper
    return decorator
