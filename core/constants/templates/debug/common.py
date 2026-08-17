from core.typing import (
    TemplateStr,
)

__all__ = [
    "TEMPLATE_DEBUG_FAILED_SERIALIZATION",
    "TEMPLATE_DEBUG_HTTP_FETCH_ATTEMPT_FAILED",
    "TEMPLATE_DEBUG_HTTP_FETCH_ATTEMPT_STARTED",
    "TEMPLATE_DEBUG_HTTP_FETCH_SUCCESS",
    "TEMPLATE_DEBUG_HTTP_FETCH_WITH_RETRY_STARTED",
    "TEMPLATE_DEBUG_LOCALE_FORMAT_INVALID",
    "TEMPLATE_DEBUG_LOCALE_LOADED",
    "TEMPLATE_DEBUG_LOCALE_LOAD_FAILED",
    "TEMPLATE_DEBUG_LOCALE_NOT_FOUND",
    "TEMPLATE_DEBUG_LOCALE_PLACEHOLDERS_MISMATCH",
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
TEMPLATE_DEBUG_LOCALE_FORMAT_INVALID: TemplateStr = (
    "[core.locale.format.invalid]: "
    "translation={translation!r}; "
    "exc_type={exc_type!r}; "
    "exc_msg={exc_msg!r}"
)
TEMPLATE_DEBUG_LOCALE_LOAD_FAILED: TemplateStr = (
    "[core.locale.load.failed]: "
    "lang={lang!r}; "
    "path={path!r}; "
    "exc_type={exc_type!r}; "
    "exc_msg={exc_msg!r}"
)
TEMPLATE_DEBUG_LOCALE_LOADED: TemplateStr = (
    "[core.locale.loaded]: "
    "lang={lang!r}; "
    "translations_count={translations_count!r}; "
    "valid_translations_count={valid_translations_count!r}"
)
TEMPLATE_DEBUG_LOCALE_NOT_FOUND: TemplateStr = (
    "[core.locale.not.found]: "
    "lang={lang!r}; "
    "path={path!r}"
)
TEMPLATE_DEBUG_LOCALE_PLACEHOLDERS_MISMATCH: TemplateStr = (
    "[core.locale.placeholders.mismatch]: "
    "source_placeholders={source_placeholders!r}; "
    "translation_placeholders={translation_placeholders!r}"
)
TEMPLATE_DEBUG_PRETTY_OBJECT: TemplateStr = (
    "[core.serialize.done]: "
    "title={title!r}; "
    "payload={payload}"
)
