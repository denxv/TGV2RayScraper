from core.typing import (
    TemplateStr,
)

__all__ = [
    "TEMPLATE_DEBUG_FAILED_SERIALIZATION",
    "TEMPLATE_DEBUG_HTTP_FETCH_ATTEMPT_FAILED",
    "TEMPLATE_DEBUG_HTTP_FETCH_ATTEMPT_STARTED",
    "TEMPLATE_DEBUG_HTTP_FETCH_SUCCESS",
    "TEMPLATE_DEBUG_HTTP_FETCH_WITH_RETRY_STARTED",
    "TEMPLATE_DEBUG_PRETTY_OBJECT",
]

TEMPLATE_DEBUG_FAILED_SERIALIZATION: TemplateStr = (
    "[core.serialize.failed]: "
    "title={title!r}; "
    "object={object!r}; "
    "exc_type={exc_type!r}; "
    "exc_msg={exc_msg!r}"
)
TEMPLATE_DEBUG_HTTP_FETCH_ATTEMPT_FAILED: TemplateStr = (
    "[http.fetch.attempt.failed]: "
    "attempt={attempt!r}; "
    "retries={retries!r}; "
    "retry_delay={retry_delay!r}; "
    "status_code={status_code!r}; "
    "url={url!r}; "
    "exc_type={exc_type!r}; "
    "exc_msg={exc_msg!r}"
)
TEMPLATE_DEBUG_HTTP_FETCH_ATTEMPT_STARTED: TemplateStr = (
    "[http.fetch.attempt.started]: "
    "attempt={attempt!r}; "
    "retries={retries!r}; "
    "url={url!r}"
)
TEMPLATE_DEBUG_HTTP_FETCH_SUCCESS: TemplateStr = (
    "[http.fetch.success]: "
    "status_code={status_code!r}; "
    "url={url!r}"
)
TEMPLATE_DEBUG_HTTP_FETCH_WITH_RETRY_STARTED: TemplateStr = (
    "[http.fetch.retry.started]: "
    "retries={retries!r}; "
    "url={url!r}"
)
TEMPLATE_DEBUG_PRETTY_OBJECT: TemplateStr = (
    "[core.serialize.done]: "
    "title={title!r}; "
    "payload={payload}"
)
