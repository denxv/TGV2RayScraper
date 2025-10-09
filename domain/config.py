from json import dumps, loads
from re import search
from urllib.parse import parse_qs, urlencode

from core.constants import (
    FORMAT_CONFIG_NAME,
    PATTERN_VMESS_JSON,
    PATTERN_URL_SS,
    PATTERN_URL_SSR_PLAIN,
    SSR_BODY_TEMPLATE,
)
from core.logger import logger
from core.typing import (
    ArgsNamespace,
    ConditionStr,
    ConfigFields,
    SortKeys,
    V2RayConfig,
    V2RayConfigs,
)
from core.utils import b64decode_safe, b64encode_safe
from domain.predicates import make_predicate


def filter_by_condition(configs: V2RayConfigs, condition: ConditionStr) -> V2RayConfigs:
    logger.info(f"Filtering {len(configs)} configs by condition: `{condition}`...")
    predicate = make_predicate(condition)
    filtered_configs = list(filter(predicate, configs))

    removed = len(configs) - len(filtered_configs)
    logger.info(
        f"Filtered: {len(filtered_configs)} configs kept, {removed} removed by condition."
    )
    return filtered_configs


def normalize(configs: V2RayConfigs) -> V2RayConfigs:
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


def normalize_config(config: V2RayConfig) -> None:
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


def normalize_config_base64(config: V2RayConfig) -> None:
    protocol = config.get("protocol", "")
    normalizers = {
        "ss": normalize_ss_base64,
        "ssr": normalize_ssr_base64,
        "vmess": normalize_vmess_base64,
    }

    if normalizer := normalizers.get(protocol):
        normalizer(config)


def normalize_ss_base64(config: V2RayConfig) -> None:
    if not (base64 := config.pop("base64", None)):
        return

    protocol = config.get("protocol", "ss")
    host = config.get("host", "").strip()
    port = config.get("port", "").strip()

    url = f"{protocol}://{b64decode_safe(base64)}"
    if host and port:
        url += f"@{host}:{port}"

    if not (ss := PATTERN_URL_SS.search(url)):
        raise Exception

    config.update(ss.groupdict(default=''))
    config.pop("base64", None)


def normalize_ssr_base64(config: V2RayConfig) -> None:
    if not (base64 := config.pop("base64", None)):
        raise Exception

    protocol = config.get("protocol", "ssr")
    url = f"{protocol}://{b64decode_safe(base64)}"

    if not (ssr := PATTERN_URL_SSR_PLAIN.search(url)):
        raise Exception

    ssr_config = ssr.groupdict(default='')
    params = ssr_config.get("params", "")

    ssr_params = {
        key: b64decode_safe(value[0])
        for key, value in parse_qs(
            params.replace('+', '%2B'),
            keep_blank_values=True,
        ).items()
    }

    ssr_params.update({
        "remarks": FORMAT_CONFIG_NAME.format(**ssr_config),
    })

    ssr_config["params"] = urlencode({
        key: b64encode_safe(value)
        for key, value in ssr_params.items()
    })

    ssr_config.update({
        "url": f"{protocol}://{b64encode_safe(SSR_BODY_TEMPLATE.format(**ssr_config))}",
        "password": b64decode_safe(ssr_config.get("password", "")),
        "params": ssr_params,
        "name": ssr_params.get("remarks", ""),
    })

    config.update(ssr_config)


def normalize_vmess_base64(config: V2RayConfig) -> None:
    if not (base64 := config.pop("base64", None)):
        return

    if not (vmess := PATTERN_VMESS_JSON.search(b64decode_safe(base64))):
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
        base64 = b64encode_safe(dumps(vmess_config, separators=(",", ":")))

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


def process_configs(configs: V2RayConfigs, args: ArgsNamespace) -> V2RayConfigs:
    if args.normalize:
        configs = normalize(configs=configs)
    if args.filter:
        configs = filter_by_condition(
            configs=configs,
            condition=args.filter,
        )
    if args.duplicate:
        configs = remove_duplicates_by_fields(
            configs=configs,
            fields=args.duplicate,
        )
    if args.sort:
        configs = sort_by_fields(
            configs=configs,
            fields=args.sort,
            reverse=args.reverse,
        )
    return configs


def remove_duplicates_by_fields(configs: V2RayConfigs, fields: ConfigFields) -> V2RayConfigs:
    logger.info(f"Removing duplicates from {len(configs)} configs using keys: {fields}...")
    if not fields:
        logger.warning("Deduplication skipped: no fields specified.")
        return configs

    seen = set()

    def is_unique(config: V2RayConfig) -> bool:
        if not all(field in config for field in fields):
            return False

        signature = tuple(config.get(field, None) for field in fields)
        if signature in seen:
            return False

        seen.add(signature)
        return True

    unique_configs = list(filter(is_unique, configs))
    removed = len(configs) - len(unique_configs)
    logger.info(
        f"Duplicate removal completed: {len(unique_configs)} configs remain, {removed} removed."
    )
    return unique_configs


def sort_by_fields(configs: V2RayConfigs, fields: ConfigFields, reverse: bool = False) -> V2RayConfigs:
    logger.info(f"Sorting {len(configs)} configs by fields: {fields} ({reverse=})...")
    if not fields:
        return configs

    def sort_key(config: V2RayConfig) -> SortKeys:
        return tuple(
            (0, value) if (value := config.get(field, None)) is not None else (1, None)
            for field in fields
        )

    sorted_configs = sorted(configs, key=sort_key, reverse=reverse)
    logger.info(f"Sorting completed: {len(sorted_configs)} configs sorted.")
    return sorted_configs
