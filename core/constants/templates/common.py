from core.constants.common import (
    TEXT_LENGTH_NAME,
    TEXT_LENGTH_NUMBER,
)
from core.typing import (
    TemplateStr,
)

__all__ = [
    "TEMPLATE_PROGRESS_DESCRIPTION",
]

TEMPLATE_PROGRESS_DESCRIPTION: TemplateStr = (
    f"{{name:<{TEXT_LENGTH_NAME}}}"
    " "
    f"{{found:+{TEXT_LENGTH_NUMBER},}}"
)
