from urllib.parse import unquote

from lxml import html
from tqdm import tqdm

from core.constants import (
    DEFAULT_COUNT,
    DEFAULT_CURRENT_ID,
    DEFAULT_FILE_CONFIGS_CLEAN,
    DEFAULT_FILE_CONFIGS_RAW,
    DEFAULT_LAST_ID,
    FORMAT_CHANNEL_PROGRESS_BAR,
    PATTERN_URL_V2RAY_ALL,
    PATTERNS_URL_ALL,
    TEMPLATE_TG_URL_AFTER,
    XPATH_TG_MESSAGES_TEXT,
)
from core.typing import (
    ChannelName,
    ChannelInfo,
    FileMode,
    FilePath,
    V2RayConfigRawIterator,
    V2RayConfigs,
    V2RayConfigsRaw,
    V2RayRawLines,
    SyncHTTPClient,
)
from core.logger import logger


def fetch_channel_configs(
    client: SyncHTTPClient,
    channel_name: ChannelName,
    channel_info: ChannelInfo,
    path_configs: FilePath = DEFAULT_FILE_CONFIGS_RAW,
) -> None:
    v2ray_count = 0
    _const_batch_ID = 20
    range_channel_id = range(
        channel_info.get("current_id", DEFAULT_CURRENT_ID),
        channel_info.get("last_id", DEFAULT_LAST_ID),
        _const_batch_ID,
    )
    logger.info(f"Extracting configs from channel '{channel_name}'...")

    for current_id in tqdm(
        range_channel_id,
        ascii=True,
        leave=False,
        bar_format=FORMAT_CHANNEL_PROGRESS_BAR,
    ):
        channel_info["current_id"] = current_id
        response = client.get(TEMPLATE_TG_URL_AFTER.format(name=channel_name, id=current_id))
        messages = html.fromstring(response.content).xpath(XPATH_TG_MESSAGES_TEXT)

        if v2ray_configs := list(filter(PATTERN_URL_V2RAY_ALL.match, messages)):
            v2ray_count = v2ray_count + len(v2ray_configs)
            channel_info["count"] = channel_info.get("count", DEFAULT_COUNT) + len(v2ray_configs)
            write_configs(
                v2ray_configs,
                path_configs=path_configs,
                mode="a",
            )

    channel_info["current_id"] = max(
        channel_info.get("last_id", DEFAULT_LAST_ID),
        DEFAULT_CURRENT_ID,
    )
    logger.info(f"Found: {v2ray_count} configs.")


def load_configs(path_configs_raw: FilePath = DEFAULT_FILE_CONFIGS_RAW) -> V2RayConfigsRaw:
    logger.info(f"Loading configs from '{path_configs_raw}'...")

    def line_to_configs(line: str) -> V2RayConfigRawIterator:
        line = unquote(line.strip())
        return (
            match.groupdict(default="")
            for pattern in PATTERNS_URL_ALL
            for match in pattern.finditer(line)
        )

    with open(path_configs_raw, "r", encoding="utf-8") as file:
        configs = [
            config
            for line in file
            for config in line_to_configs(line)
        ]

    logger.info(f"Loaded {len(configs)} configs from '{path_configs_raw}'.")
    return configs


def save_configs(
    configs: V2RayConfigs,
    path_configs_clean: FilePath = DEFAULT_FILE_CONFIGS_CLEAN,
    mode: FileMode = "w",
) -> None:
    logger.info(f"Saving {len(configs)} configs to '{path_configs_clean}'...")
    with open(path_configs_clean, mode, encoding="utf-8") as file:
        file.writelines(
            f"{config.get("url", "")}\n"
            for config in configs
        )
    logger.info(f"Saved {len(configs)} configs in '{path_configs_clean}'.")


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
