from urllib.parse import (
    unquote,
)

from lxml import (
    html,
)
from tqdm import (
    tqdm,
)

from core.constants.common import (
    BATCH_ID,
    DEFAULT_CURRENT_ID,
    DEFAULT_FILE_CONFIGS_CLEAN,
    DEFAULT_FILE_CONFIGS_RAW,
    DEFAULT_LAST_ID,
    XPATH_TG_MESSAGES_TEXT,
)
from core.constants.formats import (
    FORMAT_PROGRESS_BAR,
)
from core.constants.patterns import (
    PATTERN_V2RAY_PROTOCOLS_URL,
    PATTERNS_V2RAY_URLS_BY_PROTOCOL,
)
from core.constants.templates import (
    TEMPLATE_CHANNEL_CONFIGS_FOUND,
    TEMPLATE_CONFIG_EXTRACT_STARTED,
    TEMPLATE_CONFIG_LOAD_COMPLETED,
    TEMPLATE_CONFIG_LOAD_STARTED,
    TEMPLATE_CONFIG_SAVE_COMPLETED,
    TEMPLATE_CONFIG_SAVE_STARTED,
    TEMPLATE_ERROR_FAILED_FETCH_ID,
    TEMPLATE_ERROR_RESPONSE_EMPTY,
    TEMPLATE_FORMAT_TG_URL_AFTER,
)
from core.logger import (
    logger,
)
from core.typing import (
    ChannelInfo,
    ChannelName,
    FileMode,
    FilePath,
    SyncHTTPClient,
    V2RayConfigRawIterator,
    V2RayConfigs,
    V2RayConfigsRaw,
    V2RayRawLines,
)

__all__ = [
    "fetch_channel_configs",
    "load_configs",
    "save_configs",
    "write_configs",
]


def fetch_channel_configs(
    client: SyncHTTPClient,
    channel_name: ChannelName,
    channel_info: ChannelInfo,
    path_configs: FilePath = DEFAULT_FILE_CONFIGS_RAW,
) -> None:
    v2ray_count = 0
    range_channel_id = range(
        channel_info.get(
            "current_id",
            DEFAULT_CURRENT_ID,
        ),
        channel_info.get(
            "last_id",
            DEFAULT_LAST_ID,
        ),
        BATCH_ID,
    )

    logger.info(
        msg=TEMPLATE_CONFIG_EXTRACT_STARTED.format(
            name=channel_name,
        ),
    )

    for current_id in tqdm(
        iterable=range_channel_id,
        ascii=True,
        bar_format=FORMAT_PROGRESS_BAR,
        leave=False,
    ):
        channel_info["current_id"] = current_id

        try:
            response = client.get(
                url=TEMPLATE_FORMAT_TG_URL_AFTER.format(
                    name=channel_name,
                    id=current_id,
                ),
            )
            response.raise_for_status()

            if not response.content.strip():
                logger.debug(
                    msg=TEMPLATE_ERROR_RESPONSE_EMPTY.format(
                        current_id=current_id,
                        channel_name=channel_name,
                        status=response.status_code,
                    ),
                )
                continue

            tree = html.fromstring(
                html=response.content,
            )
            messages = tree.xpath(
                XPATH_TG_MESSAGES_TEXT,
            )
        except Exception as e:
            logger.exception(
                msg=TEMPLATE_ERROR_FAILED_FETCH_ID.format(
                    current_id=current_id,
                    channel_name=channel_name,
                    exc_type=type(e).__name__,
                    exc_msg=str(e),
                ),
            )
            continue
        else:
            configs = [
                match.group("url")
                for message in messages
                for match in PATTERN_V2RAY_PROTOCOLS_URL.finditer(
                    string=message,
                )
            ]

        if len(configs) > 0:
            v2ray_count += len(configs)
            channel_info["count"] += len(configs)

            write_configs(
                configs=configs,
                path_configs=path_configs,
                mode="a",
            )

    channel_info["current_id"] = max(
        channel_info.get(
            "last_id",
            DEFAULT_LAST_ID,
        ),
        DEFAULT_CURRENT_ID,
    )

    logger.info(
        msg=TEMPLATE_CHANNEL_CONFIGS_FOUND.format(
            count=v2ray_count,
        ),
    )


def load_configs(
    path_configs_raw: FilePath = DEFAULT_FILE_CONFIGS_RAW,
) -> V2RayConfigsRaw:
    logger.info(
        msg=TEMPLATE_CONFIG_LOAD_STARTED.format(
            path=path_configs_raw,
        ),
    )

    def line_to_configs(
        line: str,
    ) -> V2RayConfigRawIterator:
        clean_line = unquote(
            string=line.strip(),
        )

        return (
            config_match.groupdict(
                default="",
            )
            for url_match in PATTERN_V2RAY_PROTOCOLS_URL.finditer(
                string=clean_line,
            )
            for pattern in PATTERNS_V2RAY_URLS_BY_PROTOCOL.get(
                url_match.group("protocol"),
                (),
            )
            for config_match in pattern.finditer(
                string=url_match.group("url"),
            )
        )

    with open(
        file=path_configs_raw,
        encoding="utf-8",
    ) as file:
        configs = [
            config
            for line in file
            for config in line_to_configs(
                line=line,
            )
        ]

    logger.info(
        msg=TEMPLATE_CONFIG_LOAD_COMPLETED.format(
            count=len(configs),
            path=path_configs_raw,
        ),
    )

    return configs


def save_configs(
    configs: V2RayConfigs,
    path_configs_clean: FilePath = DEFAULT_FILE_CONFIGS_CLEAN,
    mode: FileMode = "w",
) -> None:
    logger.info(
        msg=TEMPLATE_CONFIG_SAVE_STARTED.format(
            count=len(configs),
            path=path_configs_clean,
        ),
    )

    with open(
        file=path_configs_clean,
        mode=mode,
        encoding="utf-8",
    ) as file:
        file.writelines(
            f"{config.get('url', '')}\n"
            for config in configs
        )

    logger.info(
        msg=TEMPLATE_CONFIG_SAVE_COMPLETED.format(
            count=len(configs),
            path=path_configs_clean,
        ),
    )


def write_configs(
    configs: V2RayRawLines,
    path_configs: FilePath = DEFAULT_FILE_CONFIGS_RAW,
    mode: FileMode = "w",
) -> None:
    with open(
        file=path_configs,
        mode=mode,
        encoding="utf-8",
    ) as file:
        file.writelines(
            f"{config}\n"
            for config in configs
        )
