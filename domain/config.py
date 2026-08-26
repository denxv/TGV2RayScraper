from dataclasses import (
    dataclass,
)
from json import (
    dumps,
    loads,
)
from urllib.parse import (
    parse_qsl,
    quote,
    unquote,
    urlencode,
)

from core.constants.common import (
    DEFAULT_JSON_INDENT,
    VMESS_TO_CONFIG_FIELD_MAPPING,
)
from core.constants.formats import (
    FORMAT_CONFIG_NAME_DEFAULT,
    FORMAT_CONFIG_NAME_PARSER,
    FORMAT_CONFIG_SSR_BODY,
    FORMAT_CONFIG_URL,
    FORMAT_CONFIG_URL_BODY,
    FORMAT_CONFIG_URL_LOCATION,
)
from core.constants.locales import (
    MESSAGE_ERROR_SSR_MISSING_BASE64,
    MESSAGE_WARNING_CHANNEL_DEDUPLICATION_SKIPPED,
    MESSAGE_WARNING_CONFIG_SORT_SKIPPED,
    TEMPLATE_ERROR_CONFIG_MISSING_REQUIRED_FIELDS,
    TEMPLATE_ERROR_CONFIG_URL_PARSE_FAILED,
    TEMPLATE_ERROR_VMESS_JSON_DECODE_FAILED,
    TEMPLATE_ERROR_VMESS_JSON_PARSE_FAILED,
    TEMPLATE_INFO_CONFIG_DEDUPLICATION_COMPLETED,
    TEMPLATE_INFO_CONFIG_DEDUPLICATION_STARTED,
    TEMPLATE_INFO_CONFIG_FILTER_COMPLETED,
    TEMPLATE_INFO_CONFIG_FILTER_STARTED,
    TEMPLATE_INFO_CONFIG_NORMALIZE_COMPLETED,
    TEMPLATE_INFO_CONFIG_NORMALIZE_STARTED,
    TEMPLATE_INFO_CONFIG_SORT_COMPLETED,
    TEMPLATE_INFO_CONFIG_SORT_STARTED,
)
from core.constants.patterns.v2ray.common import (
    PATTERN_VMESS_JSON,
)
from core.constants.patterns.v2ray.detector import (
    PATTERN_V2RAY_URL_DETECTOR,
)
from core.constants.patterns.v2ray.registry import (
    PATTERNS_V2RAY_URLS_BY_PROTOCOL,
)
from core.constants.patterns.v2ray.url import (
    PATTERN_URL_SS,
    PATTERN_URL_SSR_PLAIN,
)
from core.constants.templates.debug.config import (
    TEMPLATE_DEBUG_CONFIG_NORMALIZE_NAME_FORMAT_FAILED,
    TEMPLATE_DEBUG_CONFIG_UNEXPECTED_FAILURE,
)
from core.terminal.logger import (
    logger,
)
from core.typing import (
    ConditionStr,
    ConfigFields,
    ConfigURLGenerator,
    FormatStr,
    JSONDefault,
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
    "ConfigExtractionResult",
    "filter_by_condition",
    "format_config_name",
    "iter_formatted_config_urls",
    "line_to_configs",
    "normalize_config",
    "normalize_config_base64",
    "normalize_configs",
    "normalize_ss_base64",
    "normalize_ssr_base64",
    "normalize_vmess_base64",
    "process_configs",
    "remove_duplicates_by_fields",
    "sort_by_fields",
]


@dataclass(slots=True, frozen=True)
class ConfigExtractionResult:
    channel_name: str
    total_found: int
    new_found: int


def _dumps_config(
    config: V2RayConfig | V2RayConfigRaw,
    *,
    default: JSONDefault = str,
    ensure_ascii: bool = False,
    indent: int = DEFAULT_JSON_INDENT,
    sort_keys: bool = True,
    **kwargs: object,
) -> str:
    return dumps(
        obj=config,
        default=default,
        ensure_ascii=ensure_ascii,
        indent=indent,
        sort_keys=sort_keys,
        **kwargs,  # type: ignore[arg-type]
    )


def filter_by_condition(
    configs: V2RayConfigs,
    *,
    condition: ConditionStr,
) -> V2RayConfigs:
    logger.info(
        msg=TEMPLATE_INFO_CONFIG_FILTER_STARTED.format(
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
        msg=TEMPLATE_INFO_CONFIG_FILTER_COMPLETED.format(
            count=len(configs),
            removed=len(configs) - len(filtered_configs),
        ),
    )

    return filtered_configs


def format_config_name(
    config: V2RayConfig | V2RayConfigRaw,
    *,
    format_string: FormatStr | None = None,
) -> str:
    config_name = str(config.get("name", ""))

    if not config or format_string is None:
        return config_name

    for _format_string in (
        format_string,
        FORMAT_CONFIG_NAME_DEFAULT,
    ):
        try:
            return FORMAT_CONFIG_NAME_PARSER.format(
                _format_string,
                **config,
            )
        except (  # noqa: PERF203
            IndexError,
            KeyError,
            TypeError,
            ValueError,
        ) as e:
            logger.debug(
                msg=TEMPLATE_DEBUG_CONFIG_NORMALIZE_NAME_FORMAT_FAILED.format(
                    exc_type=type(e).__name__,
                    exc_msg=str(e),
                    format_string=_format_string,
                    config=_dumps_config(
                        config=config,
                    ),
                ),
            )

    return config_name


def iter_formatted_config_urls(
    configs: V2RayConfigs | V2RayConfigsRaw,
) -> ConfigURLGenerator:
    for config in configs:
        url = config.get("url")

        if not (url and isinstance(url, str)):
            continue

        name = config.get("name")
        protocol = config.get("protocol")

        if (
            name
            and protocol != "ssr"
            and not (
                protocol == "vmess"
                and "base64" in config
            )
        ):
            url = FORMAT_CONFIG_URL.format(
                url=url,
                name=quote(
                    string=str(name),
                    safe="%",
                ),
            )

        yield url


def line_to_configs(
    line: str,
) -> V2RayConfigRawIterator:
    return (
        config_match.groupdict(
            default="",
        )
        for url_match in PATTERN_V2RAY_URL_DETECTOR.finditer(
            string=quote(
                string=line.strip(),
                safe="%",
            ),
        )
        for pattern in PATTERNS_V2RAY_URLS_BY_PROTOCOL.get(
            url_match.group("protocol"),
            (),
        )
        for config_match in pattern.finditer(
            string=unquote(
                string=url_match.group("url"),
            ),
        )
    )


def normalize_config(
    config: V2RayConfigRaw,
    *,
    format_string: FormatStr | None = None,
) -> V2RayConfig:
    normalized_config: V2RayConfig = dict(config)

    if config.get("base64"):
        normalized_config = normalize_config_base64(
            config=config,
            format_string=format_string,
        )

    protocol = normalized_config.get("protocol", "v2ray")

    if not all(
        normalized_config.get(key)
        for key in (
            "host",
            "port",
            "protocol",
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
                        "protocol",
                        "url",
                    )
                    if not (value := normalized_config.get(key))
                ],
            ),
        )

    if isinstance(port := normalized_config.get("port"), str):
        normalized_config["port"] = int(port)

    if isinstance(params := normalized_config.get("params"), str):
        normalized_config["params"] = dict(
            parse_qsl(
                qs=params.replace("+", "%2B"),
                keep_blank_values=True,
            ),
        )

    if (
        protocol != "ssr"
        and not (
            protocol == "vmess"
            and "base64" in config
        )
    ):
        normalized_config["name"] = format_config_name(
            config=normalized_config,
            format_string=format_string,
        )

    return normalized_config


def normalize_config_base64(
    config: V2RayConfigRaw,
    *,
    format_string: FormatStr | None = None,
) -> V2RayConfig:
    normalizers = {
        "ss": normalize_ss_base64,
        "ssr": normalize_ssr_base64,
        "vmess": normalize_vmess_base64,
    }

    normalizer = normalizers.get(
        config.get("protocol", ""),
    )

    if normalizer is None:
        return dict(config)

    return normalizer(
        config=config,
        format_string=format_string,
    )


def normalize_configs(
    configs: V2RayConfigsRaw,
    *,
    format_string: FormatStr | None = None,
) -> V2RayConfigs:
    total_before = len(configs)
    logger.info(
        msg=TEMPLATE_INFO_CONFIG_NORMALIZE_STARTED.format(
            count=total_before,
        ),
    )

    normalized_configs: V2RayConfigs = []

    for config in configs:
        try:
            normalized_configs.append(
                normalize_config(
                    config=config,
                    format_string=format_string,
                ),
            )
        except Exception as e:  # noqa: PERF203
            logger.debug(
                msg=TEMPLATE_DEBUG_CONFIG_UNEXPECTED_FAILURE.format(
                    exc_type=type(e).__name__,
                    exc_msg=str(e),
                    config=_dumps_config(
                        config=config,
                    ),
                ),
            )

    total_after = len(normalized_configs)
    logger.info(
        msg=TEMPLATE_INFO_CONFIG_NORMALIZE_COMPLETED.format(
            count=total_after,
            removed=total_before - total_after,
        ),
    )

    return normalized_configs


def normalize_ss_base64(
    config: V2RayConfigRaw,
    *,
    format_string: FormatStr | None = None,  # noqa: ARG001
) -> V2RayConfig:
    if not (
        ss_base64 := config.get("base64")
    ):
        return dict(config)

    (
        host,
        port,
        path,
        params,
        name,
    ) = (
        str(config.get(key, "")).strip()
        for key in (
            "host",
            "port",
            "path",
            "params",
            "name",
        )
    )

    protocol = config.get("protocol", "ss")

    ss_url = FORMAT_CONFIG_URL_BODY.format(
        protocol=protocol,
        body=b64decode_safe(
            string=ss_base64,
        ),
    )

    if host and port:
        ss_url += FORMAT_CONFIG_URL_LOCATION.format(
            host=host,
            port=port,
        )
        ss_url += path
        ss_url += f"?{params}" if params else ""

    ss_url += f"#{name}" if name else ""

    if not (
        ss_match := PATTERN_URL_SS.search(
            string=ss_url,
        )
    ):
        raise ValueError(
            TEMPLATE_ERROR_CONFIG_URL_PARSE_FAILED.format(
                protocol=str(protocol).upper(),
            ),
        )

    ss_config: V2RayConfig = dict(config)
    ss_config.update(
        ss_match.groupdict(
            default="",
        ),
        url=config.get("url", ""),
    )

    return ss_config


def normalize_ssr_base64(
    config: V2RayConfigRaw,
    *,
    format_string: FormatStr | None = None,
) -> V2RayConfig:
    if not (
        ssr_base64 := config.get("base64")
    ):
        raise ValueError(
            MESSAGE_ERROR_SSR_MISSING_BASE64,
        )

    protocol = config.get("protocol", "ssr")

    ssr_url = FORMAT_CONFIG_URL_BODY.format(
        protocol=protocol,
        body=b64decode_safe(
            string=ssr_base64,
        ),
    )

    if not (
        ssr_match := PATTERN_URL_SSR_PLAIN.search(
            string=ssr_url,
        )
    ):
        raise ValueError(
            TEMPLATE_ERROR_CONFIG_URL_PARSE_FAILED.format(
                protocol=str(protocol).upper(),
            ),
        )

    ssr_config = ssr_match.groupdict(
        default="",
    )

    ssr_params_str = str(ssr_config.get("params", ""))
    ssr_params = {
        key: b64decode_safe(
            string=value,
        )
        for key, value in parse_qsl(
            qs=ssr_params_str.replace("+", "%2B"),
            keep_blank_values=True,
        )
    }

    ssr_config_new: V2RayConfig = dict(config)
    ssr_config_new.update(
        ssr_config,
        name=ssr_params.get("remarks", ""),
        params=ssr_params,
    )

    ssr_config_new["name"] = format_config_name(
        config=ssr_config_new,
        format_string=format_string,
    )
    ssr_params["remarks"] = str(ssr_config_new["name"])

    ssr_config["params"] = urlencode({
        key: b64encode_safe(
            string=value,
        )
        for key, value in ssr_params.items()
    })

    ssr_body_new = FORMAT_CONFIG_SSR_BODY.format_map({
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
    })
    ssr_base64_new = b64encode_safe(
        string=ssr_body_new,
    )

    ssr_config_new.update(
        base64=ssr_base64_new,
        body=ssr_body_new,
        password=b64decode_safe(
            string=ssr_config.get("password", ""),
        ),
        url=FORMAT_CONFIG_URL_BODY.format(
            protocol=protocol,
            body=ssr_base64_new,
        ),
    )

    return ssr_config_new


def normalize_vmess_base64(
    config: V2RayConfigRaw,
    *,
    format_string: FormatStr | None = None,
) -> V2RayConfig:
    if not (
        vmess_base64 := config.get("base64")
    ):
        return dict(config)

    if not (
        vmess_match := PATTERN_VMESS_JSON.search(
            string=b64decode_safe(
                string=vmess_base64,
            ),
        )
    ):
        raise ValueError(
            TEMPLATE_ERROR_VMESS_JSON_PARSE_FAILED.format(
                payload=vmess_base64,
            ),
        )

    protocol = config.get("protocol", "vmess")
    vmess_json_str = vmess_match.group("json")

    try:
        vmess_json = loads(
            s=vmess_json_str,
        )

        vmess_config: V2RayConfig = {
            **{
                target: vmess_json.get(source, "")
                for source, target in VMESS_TO_CONFIG_FIELD_MAPPING.items()
            },
            "params": {
                key: value
                for key, value in vmess_json.items()
                if key not in VMESS_TO_CONFIG_FIELD_MAPPING
            },
            "protocol": protocol,
        }

        vmess_config["name"] = format_config_name(
            config=vmess_config,
            format_string=format_string,
        )
        vmess_json["ps"] = vmess_config["name"]

        vmess_json_str_new = dumps(
            obj=vmess_json,
            separators=(",", ":"),
            sort_keys=True,
        )
        vmess_base64_new = b64encode_safe(
            string=vmess_json_str_new,
        )
    except Exception as e:
        raise ValueError(
            TEMPLATE_ERROR_VMESS_JSON_DECODE_FAILED.format(
                payload=vmess_json_str,
            ),
        ) from e

    vmess_config.update(
        base64=vmess_base64_new,
        body=vmess_json_str_new,
        url=FORMAT_CONFIG_URL_BODY.format(
            protocol=protocol,
            body=vmess_base64_new,
        ),
    )

    return vmess_config


def process_configs(
    configs: V2RayConfigs,
    *,
    config_filter: ConditionStr | None = None,
    duplicate_fields: ConfigFields | None = None,
    sort_fields: ConfigFields | None = None,
    reverse: bool = False,
) -> V2RayConfigs:
    _configs: V2RayConfigs = configs

    if config_filter:
        _configs = filter_by_condition(
            configs=_configs,
            condition=config_filter,
        )

    if duplicate_fields:
        _configs = remove_duplicates_by_fields(
            configs=_configs,
            fields=duplicate_fields,
        )

    if sort_fields:
        _configs = sort_by_fields(
            configs=_configs,
            fields=sort_fields,
            reverse=reverse,
        )

    return _configs


def remove_duplicates_by_fields(
    configs: V2RayConfigs,
    *,
    fields: ConfigFields,
) -> V2RayConfigs:
    logger.info(
        msg=TEMPLATE_INFO_CONFIG_DEDUPLICATION_STARTED.format(
            count=len(configs),
            fields=fields,
        ),
    )

    if not fields:
        logger.warning(
            msg=MESSAGE_WARNING_CHANNEL_DEDUPLICATION_SKIPPED,
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
        msg=TEMPLATE_INFO_CONFIG_DEDUPLICATION_COMPLETED.format(
            removed=len(configs) - len(unique_configs),
            remain=len(unique_configs),
        ),
    )

    return unique_configs


def sort_by_fields(
    configs: V2RayConfigs,
    *,
    fields: ConfigFields,
    reverse: bool = False,
) -> V2RayConfigs:
    logger.info(
        msg=TEMPLATE_INFO_CONFIG_SORT_STARTED.format(
            count=len(configs),
            fields=fields,
            reverse=reverse,
        ),
    )

    if not fields:
        logger.warning(
            msg=MESSAGE_WARNING_CONFIG_SORT_SKIPPED,
        )
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
        msg=TEMPLATE_INFO_CONFIG_SORT_COMPLETED.format(
            count=len(sorted_configs),
        ),
    )

    return sorted_configs
