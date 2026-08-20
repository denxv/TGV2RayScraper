# ruff: noqa: F403

from json import (
    JSONDecodeError,
    dumps,
    load,
)
from string import (
    Formatter,
)

from core.constants import (
    common as _common,
)
from core.constants.cli import *
from core.constants.messages.error import *
from core.constants.messages.info import *
from core.constants.messages.warning import *
from core.constants.tables import *
from core.constants.templates.debug import (
    common as _debug,
)
from core.constants.templates.error import *
from core.constants.templates.info.channel import *
from core.constants.templates.info.common import *
from core.constants.templates.info.config import *
from core.constants.templates.title import *
from core.terminal.logger import (
    logger,
)

_SOURCE: dict[str, str] = {
    name: value
    for name, value in globals().items()
    if (
        name.isupper()
        and not name.startswith("_")
    )
}


def _has_same_placeholders(
    *,
    source: str,
    translation: str,
) -> bool:
    try:
        source_placeholders = _parse_placeholders(
            text=source,
        )
        translation_placeholders = _parse_placeholders(
            text=translation,
        )
    except ValueError as e:
        logger.debug(
            msg=_debug.TEMPLATE_DEBUG_LOCALE_FORMAT_INVALID.format(
                translation=translation,
                exc_type=type(e).__name__,
                exc_msg=str(e),
            ),
        )
        return False
    else:
        if source_placeholders != translation_placeholders:
            logger.debug(
                msg=_debug.TEMPLATE_DEBUG_LOCALE_PLACEHOLDERS_MISMATCH.format(
                    source_placeholders=source_placeholders,
                    translation_placeholders=translation_placeholders,
                ),
            )
            return False

        return True


def _is_valid_translation(
    *,
    key: str,
    translation: object,
) -> bool:
    if (source := _SOURCE.get(key)) is None:
        return False

    if type(translation) is not type(source):
        return False

    return (
        not isinstance(translation, str)
        or _has_same_placeholders(
            source=source,
            translation=translation,
        )
    )


def _load_locale(
    *,
    lang: str = _common.CURRENT_LANG,
) -> dict[str, str]:
    path = _common.DEFAULT_PATH_LOCALES / f"{lang}.json"

    if not path.exists():
        logger.debug(
            msg=_debug.TEMPLATE_DEBUG_LOCALE_NOT_FOUND.format(
                lang=lang,
                path=str(path),
            ),
        )
        return {}

    try:
        with path.open(encoding="utf-8") as file:
            translations = load(
                fp=file,
            )
    except (
        OSError,
        JSONDecodeError,
    ) as e:
        logger.debug(
            msg=_debug.TEMPLATE_DEBUG_LOCALE_LOAD_FAILED.format(
                lang=lang,
                path=str(path),
                exc_type=type(e).__name__,
                exc_msg=str(e),
            ),
        )
        return {}
    else:
        valid_translations = {
            key: translation
            for key, translation in translations.items()
            if _is_valid_translation(
                key=key,
                translation=translation,
            )
        }
        logger.debug(
            msg=_debug.TEMPLATE_DEBUG_LOCALE_LOADED.format(
                lang=lang,
                translations_count=len(translations),
                valid_translations_count=len(valid_translations),
            ),
        )
        return valid_translations


def _parse_placeholders(
    *,
    text: str,
) -> set[tuple[str, str | None, str | None]]:
    return {
        (field, format_spec, conversion)
        for _, field, format_spec, conversion in Formatter().parse(text)
        if field is not None
    }


if _common.CURRENT_LANG != _common.DEFAULT_LANG:
    globals().update(
        _load_locale(
            lang=_common.CURRENT_LANG,
        ),
    )


if __name__ == "__main__":  # pragma: no cover
    constants_json = dumps(
        obj={
            name: value
            for name, value in sorted(
                globals().items(),
            )
            if (
                name.isupper()
                and not name.startswith("_")
            )
        },
        default=str,
        ensure_ascii=False,
        indent=_common.DEFAULT_JSON_INDENT,
    )

    logger.debug(
        msg=constants_json,
    )

    print(constants_json)  # noqa: T201
