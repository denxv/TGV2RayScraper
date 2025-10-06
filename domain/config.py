from argparse import Namespace
from json import dumps, loads
from re import DOTALL, search
from typing import Any
from urllib.parse import parse_qs, urlencode

from core.constants import FORMAT_CONFIG_NAME, SS_URL_PATTERN, SSR_PLAIN_PATTERN
from core.logger import logger
from core.utils import b64decode_safe, b64encode_safe
from domain.predicates import make_predicate


def filter_by_condition(configs: list[dict[str, Any]], condition: str) -> list[dict[str, Any]]:
    logger.info(f"Filtering {len(configs)} configs by condition: `{condition}`...")
    predicate = make_predicate(condition)
    filtered_configs = list(filter(predicate, configs))

    removed = len(configs) - len(filtered_configs) 
    logger.info(
        f"Filtered: {len(filtered_configs)} configs kept, {removed} removed by condition."
    )
    return filtered_configs


def normalize(configs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    total_before = len(configs)
    logger.info(f"Normalizing {total_before} configs...")
    for config in configs:
        try:
            normalize_config(config)
        except Exception:
            config.clear()

    normalized_configs = list(filter(None, configs))
    total_after = len(normalized_configs)
    removed = total_before - total_after
    logger.info(f"Configs normalized: {total_after} (removed: {removed}).")
    return normalized_configs


def normalize_config(config: dict[str, Any]) -> None:
    if config.get("base64"):
        normalize_config_base64(config)
    else:
        config.pop("base64", None)

    if not (config.get("host") and config.get("port") and config.get("url")):
        raise Exception

    if isinstance(port := config.get("port"), str):
        config["port"] = int(port)

    params = config.get("params", None)
    if isinstance(params, str):
        config.update({
            "params": {                      
                key: value[0] 
                for key, value in parse_qs(
                    params.replace('+', '%2B'), 
                    keep_blank_values=True, 
                ).items()
            }
        })

    if not (config.get("protocol") in ["ssr", "vmess"] and config.get("name")):
        config["name"] = FORMAT_CONFIG_NAME.format(**config)
        config["url"] = "{url}#{name}".format(**config)


def normalize_config_base64(config: dict[str, Any]) -> None:
    protocol = config.get("protocol", "")
    normalizers = {
        "ss": normalize_ss_base64,
        "ssr": normalize_ssr_base64,
        "vmess": normalize_vmess_base64,
    }

    if normalizer := normalizers.get(protocol):
        normalizer(config)


def normalize_ss_base64(config: dict[str, Any]) -> None:
    if not (base64 := config.pop("base64", None)):
        return

    protocol = config.get("protocol", "ss")
    host = config.get("host", "").strip()
    port = config.get("port", "").strip()

    url = f"{protocol}://{b64decode_safe(base64)}"
    if host and port:
        url += f"@{host}:{port}"

    if not (ss := SS_URL_PATTERN.search(url)):
        raise Exception
    
    config.update(ss.groupdict(default=''))
    config.pop("base64", None)


def normalize_ssr_base64(config: dict[str, Any]) -> None:
    if not (base64 := config.pop("base64", None)):
        raise Exception

    protocol = config.get("protocol", "ssr")
    url = f"{protocol}://{b64decode_safe(base64)}"

    if not (ssr := SSR_PLAIN_PATTERN.search(url)):
        raise Exception

    ssr_config = ssr.groupdict(default='')
    params = ssr_config.get("params", "")

    ssr_params = {                      
        key: b64decode_safe(value[0]) 
        for key, value in parse_qs(params.replace('+', '%2B'), keep_blank_values=True).items()
    }

    ssr_params.update({
        "remarks": FORMAT_CONFIG_NAME.format(**ssr_config),
    })

    ssr_config["params"] = urlencode({
        key: b64encode_safe(value)
        for key, value in ssr_params.items()
    })

    body = "{host}:{port}:{origin}:{method}:{obfs}:{password}/?{params}".format(**ssr_config)
    ssr_config.update({
        "url": f"{protocol}://{b64encode_safe(body)}",
        "password": b64decode_safe(ssr_config.get("password", "")),
        "params": ssr_params,
        "name": ssr_params.get("remarks", ""),
    })

    config.update(ssr_config)


def normalize_vmess_base64(config: dict[str, Any]) -> None:
    if not (base64 := config.pop("base64", None)):
        return

    if not (vmess := search(r'(?P<json>{.*})', b64decode_safe(base64), DOTALL)):
        raise Exception

    try:
        vmess_config = loads(vmess.group("json"))
        vmess_config.update({
            "ps": FORMAT_CONFIG_NAME.format(
                protocol=config.get("protocol", "vmess"),
                host=vmess_config.get("add", "0.0.0.0"),
                port=vmess_config.get("port", "0"),
            ),
        })
        base64 = b64encode_safe(dumps(vmess_config, separators=(',', ':')))

        config.update({
            "url": f"{config.get("protocol", "vmess")}://{base64}",
            "method": vmess_config.get("scy", ""),
            "uuid": vmess_config.get("id", ""),
            "host": vmess_config.get("add", ""),
            "port": vmess_config.get("port", ""),
            "path": vmess_config.get("path", ""),
            "params": {
                "alterId": vmess_config.get("aid", ""),
                "fp": vmess_config.get("fp", ""),
                "sni": vmess_config.get("sni", ""),
                "tls": vmess_config.get("tls", ""),
                "transport": vmess_config.get("net", ""),
                "type": vmess_config.get("type", ""),
            },
            "name": vmess_config.get("ps", ""),
        })
    except Exception:
        raise Exception


def process_configs(configs: list[dict[str, Any]], args: Namespace) -> list[dict[str, Any]]:
    if args.normalize:
        configs = normalize(configs=configs)
    if args.filter:
        configs = filter_by_condition(configs=configs, condition=args.filter)
    if args.duplicate:
        configs = remove_duplicates_by_params(configs=configs, params=args.duplicate)
    if args.sort:
        configs = sort_by_params(configs=configs, params=args.sort, reverse=args.reverse)
    return configs


def remove_duplicates_by_params(configs: list[dict[str, Any]], params: list[str]) -> list[dict[str, Any]]:
    logger.info(f"Removing duplicates from {len(configs)} configs by keys: {params}...")
    if not params:
        logger.warning("No params to deduplicate.")
        return configs

    seen = set()

    def is_unique(config: dict) -> bool:
        if not all(param in config for param in params):
            return False

        signature = tuple(config.get(param, None) for param in params)
        if signature in seen:
            return False

        seen.add(signature)
        return True

    unique_configs = list(filter(is_unique, configs))
    removed = len(configs) - len(unique_configs)
    logger.info(
        f"Duplicate removal complete: {len(unique_configs)} remain (removed: {removed}).",
    )
    return unique_configs


def sort_by_params(configs: list[dict[str, Any]], params: list[str], reverse: bool = False) -> list[dict[str, Any]]:
    logger.info(f"Sorting {len(configs)} configs by keys: {params} ({reverse=})...")
    if not params:
        return configs

    def sort_param(config: dict[str, Any]) -> tuple[tuple[int, Any | None], ...]:
        return tuple(
            (0, value) if (value := config.get(param, None)) is not None else (1, None)
            for param in params
        )

    sorted_configs = sorted(configs, key=sort_param, reverse=reverse)
    logger.info(
        f"Sorting completed. {len(sorted_configs)} configs sorted successfully.",
    )
    return sorted_configs
