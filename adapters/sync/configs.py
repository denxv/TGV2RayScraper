from urllib.parse import unquote

from lxml import html
from tqdm import tqdm

from core.constants import (
    DEFAULT_CURRENT_ID,
    DEFAULT_FILE_CONFIGS_CLEAN,
    DEFAULT_FILE_CONFIGS_RAW,
    DEFAULT_LAST_ID,
    FORMAT_CHANNEL_PROGRESS_BAR,
    PATTERN_URL_V2RAY_ALL,
    PATTERNS_URL_ALL,
    TEMPLATE_MSG_CONFIGS_FOUND,
    TEMPLATE_MSG_EXTRACTING_CONFIGS,
    TEMPLATE_MSG_LOADED_CONFIGS,
    TEMPLATE_MSG_LOADING_CONFIGS,
    TEMPLATE_MSG_SAVED_CONFIGS,
    TEMPLATE_MSG_SAVING_CONFIGS,
    TEMPLATE_TG_URL_AFTER,
    XPATH_TG_MESSAGES_TEXT,
)
from core.logger import logger
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


def fetch_channel_configs(
    client: SyncHTTPClient,
    channel_name: ChannelName,
    channel_info: ChannelInfo,
    path_configs: FilePath = DEFAULT_FILE_CONFIGS_RAW,
) -> None:
    v2ray_count = 0
    batch_id = 20
    range_channel_id = range(
        channel_info.get("current_id", DEFAULT_CURRENT_ID),
        channel_info.get("last_id", DEFAULT_LAST_ID),
        batch_id,
    )
    logger.info(TEMPLATE_MSG_EXTRACTING_CONFIGS.format(name=channel_name))

    for current_id in tqdm(
        range_channel_id,
        ascii=True,
        bar_format=FORMAT_CHANNEL_PROGRESS_BAR,
        leave=False,
    ):
        channel_info["current_id"] = current_id
        response = client.get(TEMPLATE_TG_URL_AFTER.format(
            name=channel_name,
            id=current_id,
        ))

        tree = html.fromstring(response.content)
        messages = tree.xpath(XPATH_TG_MESSAGES_TEXT)

        v2ray_configs = [
            message
            for message in messages
            if PATTERN_URL_V2RAY_ALL.match(message)
        ]

        if v2ray_configs:
            v2ray_count += len(v2ray_configs)
            channel_info["count"] += len(v2ray_configs)

            write_configs(
                configs=v2ray_configs,
                path_configs=path_configs,
                mode="a",
            )

    channel_info["current_id"] = max(
        channel_info.get("last_id", DEFAULT_LAST_ID),
        DEFAULT_CURRENT_ID,
    )

    logger.info(TEMPLATE_MSG_CONFIGS_FOUND.format(count=v2ray_count))


def load_configs(
    path_configs_raw: FilePath = DEFAULT_FILE_CONFIGS_RAW,
) -> V2RayConfigsRaw:
    logger.info(TEMPLATE_MSG_LOADING_CONFIGS.format(path=path_configs_raw))

    def line_to_configs(line: str) -> V2RayConfigRawIterator:
        clean_line = unquote(line.strip())

        return (
            match.groupdict(default="")
            for pattern in PATTERNS_URL_ALL
            for match in pattern.finditer(clean_line)
        )

    with open(path_configs_raw, encoding="utf-8") as file:
        configs = [
            config
            for line in file
            for config in line_to_configs(line)
        ]

    logger.info(TEMPLATE_MSG_LOADED_CONFIGS.format(
        count=len(configs),
        path=path_configs_raw,
    ))

    return configs


def save_configs(
    configs: V2RayConfigs,
    path_configs_clean: FilePath = DEFAULT_FILE_CONFIGS_CLEAN,
    mode: FileMode = "w",
) -> None:
    logger.info(TEMPLATE_MSG_SAVING_CONFIGS.format(
        count=len(configs),
        path=path_configs_clean,
    ))

    with open(path_configs_clean, mode, encoding="utf-8") as file:
        file.writelines(
            f"{config.get("url", "")}\n"
            for config in configs
        )

    logger.info(TEMPLATE_MSG_SAVED_CONFIGS.format(
        count=len(configs),
        path=path_configs_clean,
    ))


def write_configs(
    configs: V2RayRawLines,
    path_configs: FilePath = DEFAULT_FILE_CONFIGS_RAW,
    mode: FileMode = "w",
) -> None:
    with open(path_configs, mode, encoding="utf-8") as file:
        file.writelines(
            f"{config}\n"
            for config in configs
        )
