#!/usr/bin/env python
# coding: utf-8

import base64
import json
import re
from pathlib import Path
from typing import Any, Callable, Iterator
from urllib.parse import parse_qs, unquote, urlencode
from argparse import (
    ArgumentParser,
    ArgumentTypeError,
    HelpFormatter,
    Namespace,
    SUPPRESS,
)

from asteval import Interpreter

from logger import logger, log_debug_object

DEFAULT_PATH_CONFIGS_CLEAN = "../v2ray/configs-clean.txt"
DEFAULT_PATH_CONFIGS_RAW = "../v2ray/configs-raw.txt"
FORMAT_CONFIG_NAME = "{protocol}-{host}-{port}"

# anytls://password@host:port/path?params#name
# anytls://password@host:port?params#name
ANYTLS_URL_PATTERN = re.compile(
    r'(?P<url>'
        r'(?P<protocol>anytls)://'
        r'(?P<password>(?:(?!://).)+)'
        r'@(?P<host>[\w\-\[:%\].]+)'
        r':(?P<port>\d{1,5})'
        r'(?P<path>/[^\s?#]*){0,1}'
        r'(?:\?(?P<params>(?:(?!://)[^\s#])*)){0,1}'
        r'(?P<name>){0,1}'
    r')'
)

# hy2://password@host:port/path?params#name
# hy2://password@host:port?params#name
# hysteria2://password@host:port/path?params#name
# hysteria2://password@host:port?params#name
HYSTERIA2_URL_PATTERN = re.compile(
    r'(?P<url>'
        r'(?P<protocol>hy2|hysteria2)://'
        r'(?P<password>(?:(?!://).)+)'
        r'@(?P<host>[\w\-\[:%\].]+)'
        r':(?P<port>\d{1,5})'
        r'(?P<path>/[^\s?#]*){0,1}'
        r'(?:\?(?P<params>(?:(?!://)[^\s#])*)){0,1}'
        r'(?P<name>){0,1}'
    r')'
)

# ss://method:password@host:port#name
# ss://base64(method:password)@host:port#name
# ss://base64(method:password@host:port)#name
SS_URL_PATTERN = re.compile(
    r'(?P<url>(?P<protocol>\bss)://'
        r'(?:'
            r'(?P<method>[^\s:@#]+)'
            r':(?P<password>(?:(?!//).)+)(?=@)'
        r'|'
            r'(?P<base64>[\w+/]+={0,2})(?![^\s@#])'
        r')'
        r'(?:'
            r'@(?P<host>[\w\-\[:%\].]+)'
            r':(?P<port>\d{1,5})'
        r'){0,1}'
        r'(?=(?:[\s#]|$))(?!\?)'
        r'(?P<name>){0,1}'
    r')'
)

# ssr://base64(host:port:protocol:method:obfs:base64(password)/?param=base64(value))
SSR_URL_PATTERN = re.compile(
    r'(?P<url>'
        r'(?P<protocol>ssr)://'
        r'(?P<base64>[\w+/-]+={0,2})'
        r'(?P<name>){0,1}'
    r')'
)

# ssr://host:port:protocol:method:obfs:base64(password)/?param=base64(value)
SSR_PLAIN_PATTERN = re.compile(
    r'(?P<url>'
        r'(?P<protocol>ssr)://'
        r'(?P<host>[\w\-\[:%\].]+)'
        r':(?P<port>\d{1,5})'
        r':(?P<origin>[^\s:]+)'
        r':(?P<method>[^\s:]+)'
        r':(?P<obfs>[^\s:]+)'
        r':(?P<password>[\w+/-]+={0,2})(?=/)'
        r'(?P<path>/[^\s?#]*){0,1}'
        r'(?:\?(?P<params>(?:(?!://)[^\s#])*)){0,1}'
    r')'
)

# trojan://password@host:port/path?params#name
# trojan://password@host:port?params#name
TROJAN_URL_PATTERN = re.compile(
    r'(?P<url>'
        r'(?P<protocol>trojan)://'
        r'(?P<password>(?:(?!://).)+)'
        r'@(?P<host>[\w\-\[:%\].]+)'
        r':(?P<port>\d{1,5})'
        r'(?P<path>/[^\s?#]*){0,1}'
        r'(?:\?(?P<params>(?:(?!://)[^\s#])*)){0,1}'
        r'(?P<name>){0,1}'
    r')'
)

# tuic://uuid:password@host:port/path?params#name
# tuic://uuid:password@host:port?params#name
TUIC_URL_PATTERN = re.compile(
    r'(?P<url>'
        r'(?P<protocol>tuic)://'
        r'(?P<uuid>(?:(?!://).)+)'
        r':(?P<password>(?:(?!//).)+)'
        r'@(?P<host>[\w\-\[:%\].]+)'
        r':(?P<port>\d{1,5})'
        r'(?P<path>/[^\s?#]*){0,1}'
        r'(?:\?(?P<params>(?:(?!://)[^\s#])*)){0,1}'
        r'(?P<name>){0,1}'
    r')'
)

# vless://uuid@host:port/path?params#name
# vless://uuid@host:port?params#name
VLESS_URL_PATTERN = re.compile(
    r'(?P<url>'
        r'(?P<protocol>vless)://'
        r'(?P<uuid>(?:(?!://).)+)'
        r'@(?P<host>[\w\-\[:%\].]+)'
        r':(?P<port>\d{1,5})'
        r'(?P<path>/[^\s?#]*){0,1}'
        r'(?:\?(?P<params>(?:(?!://)[^\s#])*)){0,1}'
        r'(?P<name>){0,1}'
    r')'
)

# vmess://base64(json)
# vmess://uuid@host:port/path?params#name
# vmess://uuid@host:port?params#name
VMESS_URL_PATTERN = re.compile(
    r'(?P<url>'
        r'(?P<protocol>vmess)://'
        r'(?:'
            r'(?P<uuid>(?:(?!://).)+)'
            r'@(?P<host>[\w\-\[:%\].]+)'
            r':(?P<port>\d{1,5})'
            r'(?P<path>/[^\s?#]*){0,1}'
            r'(?:\?(?P<params>(?:(?!://)[^\s#])*)){0,1}'
            r'(?P<name>){0,1}'
        r'|'
            r'(?P<base64>[\w+/]+={0,2})'
        r')'
    r')'
)

# wireguard://privatekey@host:port/path?params#name
# wireguard://privatekey@host:port?params#name
WIREGUARD_URL_PATTERN = re.compile(
    r'(?P<url>'
        r'(?P<protocol>wireguard)://'
        r'(?P<privatekey>(?:(?!://).)+)'
        r'@(?P<host>[\w\-\[:%\].]+)'
        r':(?P<port>\d{1,5})'
        r'(?P<path>/[^\s?#]*){0,1}'
        r'(?:\?(?P<params>(?:(?!://)[^\s#])*)){0,1}'
        r'(?P<name>){0,1}'
    r')'
)

URL_PATTERNS = [
    ANYTLS_URL_PATTERN,
    HYSTERIA2_URL_PATTERN,
    SS_URL_PATTERN,
    SSR_URL_PATTERN,
    TROJAN_URL_PATTERN,
    TUIC_URL_PATTERN,
    VLESS_URL_PATTERN,
    VMESS_URL_PATTERN,
    WIREGUARD_URL_PATTERN,
]


def abs_path(path: str | Path) -> str:
    return str((Path(__file__).parent / path).resolve())


def b64decode_safe(string: str) -> str:
    if not isinstance(string, str) or not (string := string.strip()):
        return ""
    string = f"{string}{'=' * (-len(string) % 4)}"
    for b64decode in (base64.urlsafe_b64decode, base64.b64decode):
        try:
            return b64decode(string).decode('utf-8', errors='replace')
        except Exception:
            continue
    return ""


def b64encode_safe(string: str) -> str:
    return base64.b64encode(string.encode('utf-8')).decode('ascii')


def filter_by_condition(configs: list[dict[str, Any]], condition: str) -> list[dict[str, Any]]:
    logger.info(f"Filtering {len(configs)} configs by condition: `{condition}`...")
    predicate = make_predicate(condition)
    filtered_configs = list(filter(predicate, configs))

    removed = len(configs) - len(filtered_configs) 
    logger.info(
        f"Filtered: {len(filtered_configs)} configs kept, {removed} removed by condition."
    )
    return filtered_configs


def load_configs(path_configs_raw: str = "v2ray-configs-raw.txt") -> list[dict[str, Any]]:
    logger.info(f"Loading configs from '{path_configs_raw}'...")
    def line_to_configs(line: str) -> Iterator[dict[str, Any]]:
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


def make_predicate(condition: str) -> Callable[[dict[str, Any]], bool]:
    aeval = Interpreter()
    symtable = {
        "int": int,
        "len": len,
        "re_fullmatch": re_fullmatch,
        "re_search": re_search,
        "str": str,
    }

    def predicate(config: dict[str, Any]) -> bool:
        aeval.symtable.clear()
        aeval.symtable.update(symtable)
        aeval.symtable.update(config)
        try:
            return bool(aeval(condition))
        except Exception:
            return False

    return predicate


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

    if not (vmess := re.search(r'(?P<json>{.*})', b64decode_safe(base64), re.DOTALL)):
        raise Exception

    try:
        vmess_config = json.loads(vmess.group("json"))
        vmess_config.update({
            "ps": FORMAT_CONFIG_NAME.format(
                protocol=config.get("protocol", "vmess"),
                host=vmess_config.get("add", "0.0.0.0"),
                port=vmess_config.get("port", "0"),
            ),
        })
        base64 = b64encode_safe(json.dumps(vmess_config, separators=(',', ':')))

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


def parse_args() -> Namespace:
    parser = ArgumentParser(
        add_help=False,
        description="Utility to normalize, filter, deduplicate, and sort proxy configuration entries.",
        epilog=(
            "Example: python %(prog)s -I configs-raw.txt -O configs-clean.txt --filter "
            "\"re_search(r'speedtest|google', host)\" -D \"host, port\" -S \"protocol, host, port\""
        ),
        formatter_class=lambda prog: HelpFormatter(
            prog=prog,
            max_help_position=30,
            width=120,
        ),
    )

    parser.add_argument(
        "-D", "--duplicate",
        const="protocol,host,port",
        dest="duplicate",
        help=(
            "Remove duplicate entries by specified comma-separated fields. "
            "If used without value (e.g., '-D'), the default fields are '%(const)s'. "
            "If omitted, duplicates are not removed."
        ),
        metavar="FIELDS",
        nargs="?",
        type=parse_valid_params,
    )

    parser.add_argument(
        "-h", "--help",
        action="help",
        help=SUPPRESS,
    )

    parser.add_argument(
        "-F", "--filter",
        dest="filter",
        help=(
            "Filter entries using a Python-like condition. "
            "Example: \"host == '1.1.1.1' and port > 1000\". "
            "Only matching entries are kept. "
            "If omitted, no filtering is applied."
        ),
        metavar="CONDITION",
        type=str,
    )

    parser.add_argument(
        "-I", "--configs-raw",
        default=abs_path(DEFAULT_PATH_CONFIGS_RAW),
        dest="configs_raw",
        help="Path to the input file with raw V2Ray configs (default: %(default)s).",
        metavar="FILE",
        type=lambda path: validate_file_path(path, must_be_file=True),
    )

    parser.add_argument(
        "-N", "--no-normalize",
        action="store_false",
        dest="normalize",
        help="Disable normalization (enabled by default).",
    )

    parser.add_argument(
        "-O", "--configs-clean",
        default=abs_path(DEFAULT_PATH_CONFIGS_CLEAN),
        dest="configs_clean",
        help="Path to the output file for cleaned and processed configs (default: %(default)s).",
        metavar="FILE",
        type=lambda path: validate_file_path(path, must_be_file=False),
    )

    parser.add_argument(
        "-R", "--reverse",
        action="store_true",
        dest="reverse",
        help="Sort in descending order (only applies with --sort).",
    )

    parser.add_argument(
        "-S", "--sort",
        const="protocol",
        dest="sort",
        help=(
            "Sort entries by comma-separated fields. "
            "If used without value (e.g., '-S'), the default fields are '%(const)s'. "
            "If omitted, entries are not sorted."
        ),
        metavar="FIELDS",
        nargs="?",
        type=parse_valid_params,
    )

    args = parser.parse_args()
    log_debug_object("Parsed command-line arguments", args)

    return args


def parse_valid_params(params: str) -> list[str]:
    if not isinstance(params, str):
        raise ArgumentTypeError(f"Expected string, got {type(params).__name__!r}")

    seen = set()

    def check_param(param: str) -> str:
        if not re.fullmatch(r"\w+(?:\.\w+)*", param):
            raise ArgumentTypeError(f"Invalid parameter: {param!r}")
        if param in seen:
            raise ArgumentTypeError(f"Duplicate parameter: {param!r}")
        seen.add(param)
        return param

    valid_params = [
        check_param(param) 
        for param in re.split(r"[ ,]+", params.strip())
    ]

    if not valid_params:
        raise ArgumentTypeError("No parameters provided")

    return valid_params


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


def remove_duplicates_by_params(
    configs: list[dict[str, Any]],
    params: list[str],
) -> list[dict[str, Any]]:
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


def re_fullmatch(pattern: str, string: str) -> bool:
    if not isinstance(string, str):
        string = str(string)
    return bool(re.fullmatch(pattern, string))


def re_search(pattern: str, string: str) -> bool:
    if not isinstance(string, str):
        string = str(string)
    return bool(re.search(pattern, string))


def save_configs(
    configs: list[dict[str, Any]],
    path_configs_clean: str = "v2ray-configs-clean.txt",
    mode: str = "w",
) -> None:
    logger.info(f"Saving {len(configs)} configs to '{path_configs_clean}'...")
    with open(path_configs_clean, mode, encoding="utf-8") as file:
        file.writelines(f"{config.get('url', '')}\n" for config in configs)
    logger.info(f"Saved {len(configs)} configs in '{path_configs_clean}'.")


def sort_by_params(
    configs: list[dict[str, Any]],
    params: list[str],
    reverse: bool = False,
) -> list[dict[str, Any]]:
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


def validate_file_path(path: str | Path, must_be_file: bool = True) -> str:
    filepath = Path(path).resolve()

    if not filepath.parent.exists():
        raise ArgumentTypeError(f"Parent directory does not exist: '{filepath.parent}'.")

    if filepath.exists() and filepath.is_dir():
        raise ArgumentTypeError(f"'{filepath}' is a directory, expected a file.")

    if must_be_file and not filepath.is_file():
        raise ArgumentTypeError(f"The file does not exist: '{filepath}'.")
    
    return str(filepath)


def main() -> None:
    try:
        log_debug_object("List of compiled URL regex patterns", URL_PATTERNS)
        parsed_args = parse_args()
        configs = load_configs(path_configs_raw=parsed_args.configs_raw)
        configs = process_configs(configs=configs, args=parsed_args)
        save_configs(configs=configs, path_configs_clean=parsed_args.configs_clean)
    except KeyboardInterrupt:
        logger.info("Exit from the program.")
    except Exception:
        logger.exception("Unexpected error occurred.")


if __name__ == '__main__':
    main()
