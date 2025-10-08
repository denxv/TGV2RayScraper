from urllib.parse import unquote

from lxml import html
from tqdm import tqdm

from core.constants import FURL_TG_AFTER, REGEX_V2RAY, XPATH_V2RAY, URL_PATTERNS
from core.typing import (
    ChannelName,
    ChannelInfo,
    FileMode,
    FilePath,
    V2RayConfigIterator,
    V2RayConfigs,
    V2RayConfigsRaw,
    SyncSession,
)
from core.logger import logger


def fetch_channel_configs(
    session: SyncSession,
    channel_name: ChannelName,
    channel_info: ChannelInfo,
    path_configs: FilePath = "v2ray-raw.txt",
) -> None:
    v2ray_count = 0
    _const_batch_ID = 20
    bar_format = " {percentage:3.0f}% |{bar}| {n_fmt}/{total_fmt} "
    range_channel_id = range(
        channel_info.get("current_id", 0),
        channel_info.get("last_id", 0),
        _const_batch_ID,
    )
    logger.info(f"Extracting configs from channel '{channel_name}'...")

    for current_id in tqdm(range_channel_id, ascii=True, bar_format=bar_format, leave=False):
        channel_info["current_id"] = current_id
        response = session.get(FURL_TG_AFTER.format(name=channel_name, id=current_id))
        html_text = html.fromstring(response.content)

        if v2ray_configs := list(filter(REGEX_V2RAY.match, html_text.xpath(XPATH_V2RAY))):
            v2ray_count = v2ray_count + len(v2ray_configs)
            channel_info["count"] = channel_info.get("count", 0) + len(v2ray_configs)
            write_configs(
                v2ray_configs,
                path_configs=path_configs,
                mode="a",
            )
    else:
        channel_info["current_id"] = channel_info.get("last_id", 0)
        logger.info(f"Found: {v2ray_count} configs.")


def load_configs(path_configs_raw: FilePath = "v2ray-raw.txt") -> V2RayConfigs:
    logger.info(f"Loading configs from '{path_configs_raw}'...")

    def line_to_configs(line: str) -> V2RayConfigIterator:
        line = unquote(line.strip())
        return (
            match.groupdict(default='')
            for pattern in URL_PATTERNS for match in pattern.finditer(line)
        )

    with open(path_configs_raw, "r", encoding="utf-8") as file:
        configs = [
            config for line in file for config in line_to_configs(line)
        ]

    logger.info(f"Loaded {len(configs)} configs from '{path_configs_raw}'.")
    return configs


def save_configs(
    configs: V2RayConfigs,
    path_configs_clean: FilePath = "v2ray-clean.txt",
    mode: FileMode = "w",
) -> None:
    logger.info(f"Saving {len(configs)} configs to '{path_configs_clean}'...")
    with open(path_configs_clean, mode, encoding="utf-8") as file:
        file.writelines(
            f"{config.get('url', '')}\n"
            for config in configs
        )
    logger.info(f"Saved {len(configs)} configs in '{path_configs_clean}'.")


def write_configs(
    configs: V2RayConfigsRaw,
    path_configs: FilePath = "v2ray-raw.txt",
    mode: FileMode = "w",
) -> None:
    with open(path_configs, mode, encoding="utf-8") as file:
        file.writelines(f"{config}\n" for config in configs)
