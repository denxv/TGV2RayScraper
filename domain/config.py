from json import dumps, loads
from re import search
from urllib.parse import parse_qs, urlencode

from core.constants import (
    PATTERN_VMESS_JSON,
    PATTERN_URL_SS,
    PATTERN_URL_SSR_PLAIN,
    TEMPLATE_CONFIG_NAME,
    TEMPLATE_SSR_BODY,
)
from core.logger import logger
from core.typing import (
    ArgsNamespace,
    cast,
    ConditionStr,
    ConfigFields,
    SortKeys,
    V2RayConfig,
    V2RayConfigRaw,
    V2RayConfigs,
    V2RayConfigsRaw,
)
from core.utils import (
    b64decode_safe,
    b64encode_safe,
    normalize_scalar,
)
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


def normalize(configs: V2RayConfigsRaw) -> V2RayConfigs:
    total_before = len(configs)
    logger.info(f"Normalizing {total_before} configs...")

    normalized_configs: V2RayConfigs = []
    for _config in configs:
        try:
            normalized_configs.append(normalize_config(_config))
        except Exception:
            _config.clear()

    total_after = len(normalized_configs)
    removed = total_before - total_after
    logger.info(f"Configs normalized: {total_after} (removed: {removed}).")

    return normalized_configs


def normalize_config(config: V2RayConfigRaw) -> V2RayConfig:
    _config: V2RayConfig = dict(config)

    if _config.get("base64"):
        _config = normalize_config_base64(config)
    else:
        _config.pop("base64", None)

    if not (_config.get("host") and _config.get("port") and _config.get("url")):
        raise ValueError

    if isinstance(port := _config.get("port"), str):
        _config["port"] = int(port)

    params = _config.get("params", None)
    if isinstance(params, str):
        _config.update({
            "params": {
                key: value[0]
                for key, value in parse_qs(
                    params.replace('+', '%2B'),
                    keep_blank_values=True,
                ).items()
            }
        })

    if not (_config.get("protocol") in ["ssr", "vmess"] and _config.get("name")):
        _config["name"] = TEMPLATE_CONFIG_NAME.format(**_config)
        _config["url"] = "{url}#{name}".format(**_config)

    return _config


def normalize_config_base64(config: V2RayConfigRaw) -> V2RayConfig:
    normalizers = {
        "ss": normalize_ss_base64,
        "ssr": normalize_ssr_base64,
        "vmess": normalize_vmess_base64,
    }

    if normalizer := normalizers.get(config.get("protocol", "")):
        return normalizer(config)

    return dict(config)


def normalize_ss_base64(config: V2RayConfigRaw) -> V2RayConfig:
    if not (base64 := config.pop("base64", None)):
        return dict(config)

    protocol = config.get("protocol", "ss")
    host = config.get("host", "").strip()
    port = config.get("port", "").strip()

    url = f"{protocol}://{b64decode_safe(base64)}"
    if host and port:
        url += f"@{host}:{port}"

    if not (ss := PATTERN_URL_SS.search(url)):
        raise ValueError

    _config: V2RayConfig = dict(config)
    _config.update(ss.groupdict(default=""))
    _config.pop("base64", None)

    return _config


def normalize_ssr_base64(config: V2RayConfigRaw) -> V2RayConfig:
    if not (base64 := config.pop("base64", None)):
        raise ValueError

    protocol = config.get("protocol", "ssr")
    url = f"{protocol}://{b64decode_safe(base64)}"

    if not (ssr := PATTERN_URL_SSR_PLAIN.search(url)):
        raise ValueError

    ssr_config = ssr.groupdict(default="")
    params = ssr_config.get("params", "")

    ssr_params = {
        key: b64decode_safe(value[0])
        for key, value in parse_qs(
            params.replace('+', '%2B'),
            keep_blank_values=True,
        ).items()
    }

    ssr_params.update({
        "remarks": TEMPLATE_CONFIG_NAME.format(**ssr_config),
    })

    ssr_config["params"] = urlencode({
        key: b64encode_safe(value)
        for key, value in ssr_params.items()
    })

    ssr_config.update({
        "url": f"{protocol}://{b64encode_safe(TEMPLATE_SSR_BODY.format(**ssr_config))}",
        "password": b64decode_safe(ssr_config.get("password", "")),
        "name": ssr_params.get("remarks", ""),
    })

    _config: V2RayConfig = dict(config)
    _config.update({
        **ssr_config,
        "params": ssr_params,
    })

    return _config


def normalize_vmess_base64(config: V2RayConfigRaw) -> V2RayConfig:
    if not (base64 := config.pop("base64", None)):
        return dict(config)

    if not (vmess := PATTERN_VMESS_JSON.search(b64decode_safe(base64))):
        raise ValueError

    try:
        vmess_config = loads(vmess.group("json"))
        vmess_config.update({
            "ps": TEMPLATE_CONFIG_NAME.format(
                protocol=config.get("protocol", "vmess"),
                host=vmess_config.get("add", "0.0.0.0"),
                port=vmess_config.get("port", "0"),
            ),
        })
        base64 = b64encode_safe(dumps(vmess_config, separators=(",", ":")))
    except Exception:
        raise ValueError

    return {
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
    }


def process_configs(configs: V2RayConfigsRaw, args: ArgsNamespace) -> V2RayConfigs:
    _configs: V2RayConfigs = cast(V2RayConfigs, configs)

    if args.normalize:
        _configs = normalize(
            configs=configs,
        )

    if args.filter:
        _configs = filter_by_condition(
            configs=_configs,
            condition=args.filter,
        )

    if args.duplicate:
        _configs = remove_duplicates_by_fields(
            configs=_configs,
            fields=args.duplicate,
        )

    if args.sort:
        _configs = sort_by_fields(
            configs=_configs,
            fields=args.sort,
            reverse=args.reverse,
        )

    return _configs


def remove_duplicates_by_fields(configs: V2RayConfigs, fields: ConfigFields) -> V2RayConfigs:
    logger.info(f"Removing duplicates from {len(configs)} configs using keys: {fields}...")
    if not fields:
        logger.warning("Deduplication skipped: no fields specified.")
        return configs

    seen = set()

    def is_unique(config: V2RayConfig) -> bool:
        if not all(field in config for field in fields):
            return False

        _signature = tuple(
            normalize_scalar(config.get(field, None))
            for field in fields
        )

        if _signature in seen:
            return False

        seen.add(_signature)
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
        _values = []

        for field in fields:
            value = config.get(field, None)
            if value is not None:
                _values.append((0, normalize_scalar(value)))
            else:
                _values.append((1, None))

        return tuple(_values)

    sorted_configs = sorted(configs, key=sort_key, reverse=reverse)
    logger.info(f"Sorting completed: {len(sorted_configs)} configs sorted.")
    return sorted_configs
