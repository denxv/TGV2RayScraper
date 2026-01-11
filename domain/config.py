from json import (
    dumps,
    loads,
)
from urllib.parse import (
    parse_qsl,
    unquote,
    urlencode,
)

from core.constants.common import (
    DEFAULT_JSON_INDENT,
)
from core.constants.messages import (
    MESSAGE_CHANNEL_DEDUPLICATION_SKIPPED,
    MESSAGE_ERROR_SSR_MISSING_BASE64,
)
from core.constants.patterns import (
    PATTERN_URL_SS,
    PATTERN_URL_SSR_PLAIN,
    PATTERN_V2RAY_PROTOCOLS_URL,
    PATTERN_VMESS_JSON,
    PATTERNS_V2RAY_URLS_BY_PROTOCOL,
)
from core.constants.templates import (
    TEMPLATE_CONFIG_DEDUPLICATION_COMPLETED,
    TEMPLATE_CONFIG_DEDUPLICATION_STARTED,
    TEMPLATE_CONFIG_FILTER_COMPLETED,
    TEMPLATE_CONFIG_FILTER_STARTED,
    TEMPLATE_CONFIG_NORMALIZE_COMPLETED,
    TEMPLATE_CONFIG_NORMALIZE_STARTED,
    TEMPLATE_CONFIG_SORT_COMPLETED,
    TEMPLATE_CONFIG_SORT_STARTED,
    TEMPLATE_ERROR_CONFIG_MISSING_REQUIRED_FIELDS,
    TEMPLATE_ERROR_CONFIG_UNEXPECTED_FAILURE,
    TEMPLATE_ERROR_CONFIG_URL_PARSE_FAILED,
    TEMPLATE_ERROR_VMESS_JSON_DECODE_FAILED,
    TEMPLATE_ERROR_VMESS_JSON_PARSE_FAILED,
    TEMPLATE_FORMAT_CONFIG_NAME,
    TEMPLATE_FORMAT_CONFIG_SSR_BODY,
    TEMPLATE_FORMAT_CONFIG_URL,
    TEMPLATE_FORMAT_CONFIG_URL_BODY,
    TEMPLATE_FORMAT_CONFIG_URL_LOCATION,
)
from core.logger import (
    logger,
)
from core.typing import (
    ArgsNamespace,
    ConditionStr,
    ConfigFields,
    SortKeys,
    V2RayConfig,
    V2RayConfigRaw,
    V2RayConfigRawIterator,
    V2RayConfigs,
    V2RayConfigsRaw,
)
from core.utils import (
    b64decode_safe,
    b64encode_safe,
    normalize_scalar,
)
from domain.predicates import (
    make_predicate,
)

__all__ = [
    "filter_by_condition",
    "line_to_configs",
    "normalize",
    "normalize_config",
    "normalize_config_base64",
    "normalize_ss_base64",
    "normalize_ssr_base64",
    "normalize_vmess_base64",
    "process_configs",
    "remove_duplicates_by_fields",
    "sort_by_fields",
]


def filter_by_condition(
    configs: V2RayConfigs,
    condition: ConditionStr,
) -> V2RayConfigs:
    logger.info(
        msg=TEMPLATE_CONFIG_FILTER_STARTED.format(
            count=len(configs),
            condition=condition,
        ),
    )

    filtered_configs = list(
        filter(
            make_predicate(
                condition=condition,
            ),
            configs,
        ),
    )

    logger.info(
        msg=TEMPLATE_CONFIG_FILTER_COMPLETED.format(
            count=len(configs),
            removed=len(configs) - len(filtered_configs),
        ),
    )

    return filtered_configs


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


def normalize(
    configs: V2RayConfigsRaw,
) -> V2RayConfigs:
    total_before = len(configs)
    logger.info(
        msg=TEMPLATE_CONFIG_NORMALIZE_STARTED.format(
            count=total_before,
        ),
    )

    normalized_configs: V2RayConfigs = []

    for _config in configs:
        try:
            normalized_configs.append(
                normalize_config(
                    config=_config,
                ),
            )
        except Exception as e:  # noqa: PERF203
            logger.debug(
                msg=TEMPLATE_ERROR_CONFIG_UNEXPECTED_FAILURE.format(
                    config=dumps(
                        obj=_config,
                        default=str,
                        ensure_ascii=False,
                        indent=DEFAULT_JSON_INDENT,
                        sort_keys=True,
                    ),
                    exc_type=type(e).__name__,
                    exc_msg=str(e),
                ),
            )

    total_after = len(normalized_configs)
    logger.info(
        msg=TEMPLATE_CONFIG_NORMALIZE_COMPLETED.format(
            count=total_after,
            removed=total_before - total_after,
        ),
    )

    return normalized_configs


def normalize_config(
    config: V2RayConfigRaw,
) -> V2RayConfig:
    _config: V2RayConfig = dict(config)

    if config.get("base64"):
        _config = normalize_config_base64(
            config=config,
        )
    else:
        _config.pop("base64", None)

    protocol = _config.get("protocol", "")

    if not all(
        _config.get(key)
        for key in (
            "host",
            "port",
            "url",
        )
    ):
        raise ValueError(
            TEMPLATE_ERROR_CONFIG_MISSING_REQUIRED_FIELDS.format(
                protocol=str(protocol).upper(),
                fields=[
                    (
                        key,
                        value,
                    )
                    for key in (
                        "host",
                        "port",
                        "url",
                    )
                    if not (value := _config.get(key))
                ],
            ),
        )

    if isinstance(port := _config.get("port"), str):
        _config["port"] = int(port)

    if isinstance(params := _config.get("params"), str):
        _config.update({
            "params": dict(
                parse_qsl(
                    qs=params.replace("+", "%2B"),
                    keep_blank_values=True,
                ),
            ),
        })

    if (
        not (
            protocol in (
                "ssr",
                "vmess",
            )
            and _config.get("name", "")
        )
    ):
        _config["name"] = TEMPLATE_FORMAT_CONFIG_NAME.format_map({
            key: _config.get(key, "*")
            for key in (
                "protocol",
                "host",
                "port",
            )
        })
        _config["url"] = TEMPLATE_FORMAT_CONFIG_URL.format_map({
            key: _config.get(key, "*")
            for key in (
                "url",
                "name",
            )
        })

    return _config


def normalize_config_base64(
    config: V2RayConfigRaw,
) -> V2RayConfig:
    normalizers = {
        "ss": normalize_ss_base64,
        "ssr": normalize_ssr_base64,
        "vmess": normalize_vmess_base64,
    }

    if normalizer := normalizers.get(
        config.get("protocol", ""),
    ):
        return normalizer(config)

    return dict(config)


def normalize_ss_base64(
    config: V2RayConfigRaw,
) -> V2RayConfig:
    if not (
        base64 := config.pop("base64", None)
    ):
        return dict(config)

    (
        protocol,
        host,
        port,
        path,
        params,
    ) = (
        config.get(
            key,
            "ss" if key == "protocol" else "",
        ).strip()
        for key in (
            "protocol",
            "host",
            "port",
            "path",
            "params",
        )
    )

    url = TEMPLATE_FORMAT_CONFIG_URL_BODY.format(
        protocol=protocol,
        body=b64decode_safe(
            string=base64,
        ),
    )
    if host and port:
        url += TEMPLATE_FORMAT_CONFIG_URL_LOCATION.format(
            host=host,
            port=port,
        )
        url += path
        url += f"?{params}" if params else ""

    if not (
        ss := PATTERN_URL_SS.search(
            string=url,
        )
    ):
        raise ValueError(
            TEMPLATE_ERROR_CONFIG_URL_PARSE_FAILED.format(
                protocol=str(protocol).upper(),
                url=url,
            ),
        )

    _config: V2RayConfig = dict(config)
    _config.update(
        ss.groupdict(
            default="",
        ),
    )

    return _config


def normalize_ssr_base64(
    config: V2RayConfigRaw,
) -> V2RayConfig:
    if not (
        base64 := config.pop("base64", None)
    ):
        raise ValueError(
            MESSAGE_ERROR_SSR_MISSING_BASE64,
        )

    protocol = config.get("protocol", "ssr")
    url = TEMPLATE_FORMAT_CONFIG_URL_BODY.format(
        protocol=protocol,
        body=b64decode_safe(
            string=base64,
        ),
    )

    if not (
        ssr := PATTERN_URL_SSR_PLAIN.search(
            string=url,
        )
    ):
        raise ValueError(
            TEMPLATE_ERROR_CONFIG_URL_PARSE_FAILED.format(
                protocol=str(protocol).upper(),
                url=url,
            ),
        )

    ssr_config = ssr.groupdict(
        default="",
    )
    params = ssr_config.get("params", "")

    ssr_params = {
        key: b64decode_safe(
            string=value,
        )
        for key, value in parse_qsl(
            qs=params.replace(
                "+",
                "%2B",
            ),
            keep_blank_values=True,
        )
    }
    ssr_params.update({
        "remarks": TEMPLATE_FORMAT_CONFIG_NAME.format_map({
            key: ssr_config.get(key, "*")
            for key in (
                "protocol",
                "host",
                "port",
            )
        }),
    })
    ssr_config["params"] = urlencode({
        key: b64encode_safe(
            string=value,
        )
        for key, value in ssr_params.items()
    })

    base64 = b64encode_safe(
        string=TEMPLATE_FORMAT_CONFIG_SSR_BODY.format_map({
            key: ssr_config.get(key, "")
            for key in (
                "host",
                "port",
                "origin",
                "method",
                "obfs",
                "password",
                "params",
            )
        }),
    )
    ssr_config.update({
        "url": TEMPLATE_FORMAT_CONFIG_URL_BODY.format(
            protocol=protocol,
            body=base64,
        ),
        "password": b64decode_safe(
            string=ssr_config.get("password", ""),
        ),
        "name": ssr_params.get("remarks", ""),
    })

    _config: V2RayConfig = dict(config)
    _config.update({
        **ssr_config,
        "params": ssr_params,
    })

    return _config


def normalize_vmess_base64(
    config: V2RayConfigRaw,
) -> V2RayConfig:
    if not (
        base64 := config.pop("base64", None)
    ):
        return dict(config)

    if not (
        vmess := PATTERN_VMESS_JSON.search(
            string=b64decode_safe(
                string=base64,
            ),
        )
    ):
        raise ValueError(
            TEMPLATE_ERROR_VMESS_JSON_PARSE_FAILED.format(
                base64=base64,
            ),
        )

    try:
        protocol = config.get("protocol", "vmess")

        vmess_config = loads(
            s=vmess.group("json"),
        )
        vmess_config.update({
            "ps": TEMPLATE_FORMAT_CONFIG_NAME.format(
                protocol=protocol,
                host=vmess_config.get("add", "255.255.255.255"),
                port=vmess_config.get("port", "0"),
            ),
        })

        base64 = b64encode_safe(
            dumps(
                obj=vmess_config,
                separators=(",", ":"),
            ),
        )
    except Exception as e:
        raise ValueError(
            TEMPLATE_ERROR_VMESS_JSON_DECODE_FAILED.format(
                json=vmess.group("json"),
            ),
        ) from e

    return {
        "url": TEMPLATE_FORMAT_CONFIG_URL_BODY.format(
            protocol=protocol,
            body=base64,
        ),
        "protocol": protocol,
        "method": vmess_config.get("scy", ""),
        "uuid": vmess_config.get("id", ""),
        "host": vmess_config.get("add", ""),
        "port": vmess_config.get("port", ""),
        "path": vmess_config.get("path", ""),
        "params": {
            key: vmess_config.get(key, "")
            for key in (
                "aid",
                "fp",
                "host",
                "insecure",
                "net",
                "sni",
                "tls",
                "type",
                "v",
            )
        },
        "name": vmess_config.get("ps", ""),
    }


def process_configs(
    configs: V2RayConfigsRaw,
    args: ArgsNamespace,
) -> V2RayConfigs:
    _configs: V2RayConfigs = configs  # type: ignore[assignment]

    if args.normalize:
        _configs = normalize(
            configs=configs,
        )

    if args.config_filter:
        _configs = filter_by_condition(
            configs=_configs,
            condition=args.config_filter,
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


def remove_duplicates_by_fields(
    configs: V2RayConfigs,
    fields: ConfigFields,
) -> V2RayConfigs:
    logger.info(
        msg=TEMPLATE_CONFIG_DEDUPLICATION_STARTED.format(
            count=len(configs),
            fields=fields,
        ),
    )

    if not fields:
        logger.warning(
            msg=MESSAGE_CHANNEL_DEDUPLICATION_SKIPPED,
        )
        return configs

    seen = set()

    def is_unique(
        config: V2RayConfig,
    ) -> bool:
        if not all(
            field in config
            for field in fields
        ):
            return False

        _signature = tuple(
            normalize_scalar(
                value=config.get(field),
            )
            for field in fields
        )

        if _signature in seen:
            return False

        seen.add(_signature)

        return True

    unique_configs = list(
        filter(is_unique, configs),
    )

    logger.info(
        msg=TEMPLATE_CONFIG_DEDUPLICATION_COMPLETED.format(
            remain=len(unique_configs),
            removed=len(configs) - len(unique_configs),
        ),
    )

    return unique_configs


def sort_by_fields(
    configs: V2RayConfigs,
    fields: ConfigFields,
    *,
    reverse: bool = False,
) -> V2RayConfigs:
    logger.info(
        msg=TEMPLATE_CONFIG_SORT_STARTED.format(
            count=len(configs),
            fields=fields,
            reverse=reverse,
        ),
    )

    if not fields:
        return configs

    def sort_key(
        config: V2RayConfig,
    ) -> SortKeys:
        _values = []

        for field in fields:
            value = config.get(field)

            if value is not None:
                _values.append((
                    0,
                    normalize_scalar(
                        value=value,
                    ),
                ))
            else:
                _values.append((
                    1,
                    None,
                ))

        return tuple(_values)

    sorted_configs = sorted(
        configs,
        key=sort_key,
        reverse=reverse,
    )

    logger.info(
        msg=TEMPLATE_CONFIG_SORT_COMPLETED.format(
            count=len(sorted_configs),
        ),
    )

    return sorted_configs
