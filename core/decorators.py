from functools import wraps

from core.typing import AnyFunc, FuncDecorator, P, T
from core.logger import logger


def status(start: str, end: str = "", tracking: bool = False) -> FuncDecorator[P, T]:
    def decorator(target_func: AnyFunc[P, T]) -> AnyFunc[P, T]:
        @wraps(target_func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            logger.info(start)
            first_value = args[0] if args else next(iter(kwargs.values()), None)
            old_size = len(first_value) if tracking and isinstance(first_value, dict) else None
            result = target_func(*args, **kwargs)
            if tracking and old_size is not None:
                new_size = len(result)
                diff = new_size - old_size
                logger.info(f"Old count: {old_size} | New count: {new_size} | ({diff:+})")
            if end:
                logger.info(end)
            return result
        return wrapper
    return decorator
