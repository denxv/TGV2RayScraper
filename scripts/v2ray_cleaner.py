#!/usr/bin/env python
# coding: utf-8

import base64
import json
import re
from argparse import ArgumentParser, ArgumentTypeError, HelpFormatter, Namespace 
from asteval import Interpreter
from pathlib import Path
from typing import Any, Callable, Iterator
from urllib.parse import parse_qs, unquote

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
        r'(?:#(?P<name>[^\s/]*)){0,1}'
    r')'
)

# hy2://password@host:port/path?params#name
# hy2://password@host:port?params#name
# hysteria2://password@host:port/path?params#name
# hysteria2://password@host:port?params#name
HYSTERIA2_URL_PATTERN = re.compile(
    r'(?P<url>'
        r'(?P<protocol>hy2\b|hysteria2\b)://'
        r'(?P<password>(?:(?!://).)+)'
        r'@(?P<host>[\w\-\[:%\].]+)'
        r':(?P<port>\d{1,5})'
        r'(?P<path>/[^\s?#]*){0,1}'
        r'(?:\?(?P<params>(?:(?!://)[^\s#])*)){0,1}'
        r'(?:#(?P<name>[^\s/]*)){0,1}'
    r')'
)

# ss://method:password@host:port#name
# ss://base64(method:password)@host:port#name
# ss://base64(method:password@host:port)#name
SS_URL_PATTERN = re.compile(
    r'(?P<url>(?P<protocol>\bss\b)://'
        r'(?:'
            r'(?P<method>[^\s:@#]+)'
            r':(?P<password>(?:(?!://).)+)(?=@)'
        r'|'
            r'(?P<base64>[\w+/]+={0,2})(?![^\s@#])'
        r')'
        r'(?:'
            r'@(?P<host>[\w\-\[:%\].]+)'
            r':(?P<port>\d{1,5})'
        r'){0,1}'
        r'(?=(?:[\s#]|$))(?!\?)'
        r'(?:#(?P<name>[^\s/]*)){0,1}'
    r')'
)

# ssr://base64(host:port:protocol:method:obfs:base64(password)/?param=base64(value))
SSR_URL_PATTERN = re.compile(
    r'(?P<url>'
        r'(?P<protocol>\bssr\b)://'
        r'(?P<base64>[\w+/-]+={0,2})'
        r'(?:#(?P<name>[^\s/]*)){0,1}'
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
        r'(?P<protocol>trojan\b)://'
        r'(?P<password>(?:(?!://).)+)'
        r'@(?P<host>[\w\-\[:%\].]+)'
        r':(?P<port>\d{1,5})'
        r'(?P<path>/[^\s?#]*){0,1}'
        r'(?:\?(?P<params>(?:(?!://)[^\s#])*)){0,1}'
        r'(?:#(?P<name>[^\s/]*)){0,1}'
    r')'
)

# tuic://uuid:password@host:port/path?params#name
# tuic://uuid:password@host:port?params#name
TUIC_URL_PATTERN = re.compile(
    r'(?P<url>'
        r'(?P<protocol>tuic)://'
        r'(?P<uuid>(?:(?!://).)+)'
        r':(?P<password>(?:(?!://).)+)'
        r'@(?P<host>[\w\-\[:%\].]+)'
        r':(?P<port>\d{1,5})'
        r'(?P<path>/[^\s?#]*){0,1}'
        r'(?:\?(?P<params>(?:(?!://)[^\s#])*)){0,1}'
        r'(?:#(?P<name>[^\s/]*)){0,1}'
    r')'
)

# vless://uuid@host:port/path?params#name
# vless://uuid@host:port?params#name
VLESS_URL_PATTERN = re.compile(
    r'(?P<url>'
        r'(?P<protocol>vless\b)://'
        r'(?P<uuid>(?:(?!://).)+)'
        r'@(?P<host>[\w\-\[:%\].]+)'
        r':(?P<port>\d{1,5})'
        r'(?P<path>/[^\s?#]*){0,1}'
        r'(?:\?(?P<params>(?:(?!://)[^\s#])*)){0,1}'
        r'(?:#(?P<name>[^\s/]*)){0,1}'
    r')'
)

# vmess://base64(json)
# vmess://uuid@host:port/path?params#name
# vmess://uuid@host:port?params#name
VMESS_URL_PATTERN = re.compile(
    r'(?P<url>'
        r'(?P<protocol>vmess\b)://'
        r'(?:'
            r'(?P<uuid>(?:(?!://).)+)'
            r'@(?P<host>[\w\-\[:%\].]+)'
            r':(?P<port>\d{1,5})'
            r'(?P<path>/[^\s?#]*){0,1}'
            r'(?:\?(?P<params>(?:(?!://)[^\s#])*)){0,1}'
            r'(?:#(?P<name>[^\s/]*)){0,1}'
        r'|'
            r'(?P<base64>[\w+/]+={0,2})'
        r')'
    r')'
)

# wireguard://privatekey@host:port/path?params#name
# wireguard://privatekey@host:port?params#name
WIREGUARD_URL_PATTERN = re.compile(
    r'(?P<url>'
        r'(?P<protocol>wireguard\b)://'
        r'(?P<privatekey>(?:(?!://).)+)'
        r'@(?P<host>[\w\-\[:%\].]+)'
        r':(?P<port>\d{1,5})'
        r'(?P<path>/[^\s?#]*){0,1}'
        r'(?:\?(?P<params>(?:(?!://)[^\s#])*)){0,1}'
        r'(?:#(?P<name>[^\s/]*)){0,1}'
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


def abs_path(path: str) -> str:
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


def existing_file(path: str) -> str:
    filepath = Path(path).resolve()
    if not filepath.is_file():
        raise ArgumentTypeError(f"The file does not exist: {filepath}")
    return str(filepath)


def filter_by_condition(configs: list[dict[str, Any]], condition: str) -> list[dict[str, Any]]:
    print(f"[FILT] Filtering {len(configs)} configs by condition: `{condition}`...")
    predicate = make_predicate(condition)
    filtered_configs = list(filter(predicate, configs))

    removed = len(configs) - len(filtered_configs) 
    print(
        f"[FILT] Filtered: {len(filtered_configs)} configs kept, "
        f"{removed} removed by condition.", 
        end="\n\n",
    )
    return filtered_configs


def load_configs(path_configs_raw: str = "v2ray-configs-raw.txt") -> list[dict[str, Any]]:
    print(f"[LOAD] Loading configs...")
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

    print(
        f"[LOAD] Loaded {len(configs)} configs from '{path_configs_raw}'.", 
        end="\n\n",
    )
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
    print(f"[NORM] Normalizing {total_before} configs...")
    for config in configs:
        try:
            normalize_config(config)
        except Exception:
            config.clear()

    normalized_configs = list(filter(None, configs))
    total_after = len(normalized_configs)
    removed = total_before - total_after
    print(
        f"[NORM] Configs normalized: {total_after} "
        f"(removed: {removed}).", 
        end="\n\n",
    )
    return normalized_configs


def normalize_config(config: dict[str, Any]) -> None:
    if "base64" in config:
        normalize_config_base64(config)

    if isinstance(port := config.get("port", ""), str):
        config["port"] = int(port)

    if not (config.get("host") and config.get("port")):
        config.clear()

    params = config.get("params", None)
    if isinstance(params, str):
        config.update({
            "params": {                      
                key: value[0] 
                for key, value in parse_qs(params.replace('+', '%2B'), \
                    keep_blank_values=True).items()
            }
        })


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
    protocol = config.get("protocol", "")
    base64 = config.pop("base64", "")
    host = config.get("host", "").strip()
    port = config.get("port", "").strip()
    name = config.get("name", "").strip()

    url = f"{protocol}://{b64decode_safe(base64)}{f'@{host}:{port}' if host and port else ''}#{name}"
    if ss := SS_URL_PATTERN.search(url):
        config.update(ss.groupdict(default=''))
        config.pop("base64", None)
    else:
        config.clear()


def normalize_ssr_base64(config: dict[str, Any]) -> None:
    protocol = config.get("protocol", "")
    base64 = config.pop("base64", "")
    url = f"{protocol}://{b64decode_safe(base64)}"

    if (ssr := SSR_PLAIN_PATTERN.search(url)):
        ssr_config = ssr.groupdict(default='')
        ssr_config.pop("url", "")
        params = ssr_config.get("params", "")
        ssr_config.update({
            "password": b64decode_safe(ssr_config.get("password", "")),
            "params": {                      
                key: b64decode_safe(value[0]) 
                for key, value in parse_qs(params, keep_blank_values=True).items()
            }
        })

        ssr_config.update({
            "name": ssr_config.get("params", {}).get("remarks", "")
        })

        config.update(ssr_config)


def normalize_vmess_base64(config: dict[str, Any]) -> None:
    if not (vmess_config := repair_broken_vmess(config)):
        return

    config.update({
        "url": vmess_config.get("url", ""),
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


def remove_duplicates_by_params(configs: list[dict[str, Any]], \
    params: list[str]) -> list[dict[str, Any]]:
    print(f"[DUPL] Removing duplicates from {len(configs)} configs by keys: {params}...")
    if not params:
        print("[DUPL] No params to deduplicate.", end="\n\n")
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
    print(
        f"[DUPL] Duplicate removal complete: "
        f"{len(unique_configs)} remain (removed: {removed}).",
        end="\n\n",
    )
    return unique_configs


def repair_broken_vmess(config: dict[str, Any]) -> dict[str, Any] | None:
    if not (base64 := config.pop("base64", "")):
        return

    if not (vmess := re.search(r'(?P<json>{.*})', b64decode_safe(base64), re.DOTALL)):
        config.clear()
        return

    try:
        vmess_config = json.loads(vmess.group("json"))
        base64 = b64encode_safe(json.dumps(vmess_config, separators=(',', ':')))
        vmess_config.update({"url": f"{config.get("protocol", "vmess")}://{base64}"})
        return vmess_config
    except Exception:
        config.clear()
        return


def re_fullmatch(pattern: str, string: str) -> bool:
    if not isinstance(string, str):
        string = str(string)
    return bool(re.fullmatch(pattern, string))


def re_search(pattern: str, string: str) -> bool:
    if not isinstance(string, str):
        string = str(string)
    return bool(re.search(pattern, string))


def parse_args() -> Namespace:
    raw_rel_path = "../v2ray/configs-raw.txt"
    clean_rel_path = "../v2ray/configs-clean.txt"

    parser = ArgumentParser(
        description="Utility to normalize, filter, deduplicate, and sort proxy configuration entries.",
        epilog="Example: python %(prog)s --filter \"host == '1.1.1.1'\" --duplicate --sort",
        formatter_class=lambda prog: HelpFormatter(
            prog=prog,
            max_help_position=30,
            width=120,
        ),
    )

    parser.add_argument(
        "-D", "--duplicate",
        const="protocol,host,port",
        default=None,
        dest="duplicate",
        help=(
            "Remove duplicate entries by specified comma-separated fields. "
            "If used without value (e.g., '-D'), the default fields are '%(const)s'. "
            "If omitted, duplicates are not removed."
        ),
        metavar="FIELDS",
        nargs="?",
        type=split_valid_params,
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
        "-I", "--input",
        default=abs_path(raw_rel_path),
        dest="input",
        help="Path to the file with raw configs (default: %(default)s).",
        metavar="FILE",
        type=existing_file,
    )

    parser.add_argument(
        "-N", "--no-normalize",
        action="store_false",
        dest="normalize",
        help="Disable normalization (enabled by default).",
    )

    parser.add_argument(
        "-O", "--output",
        default=abs_path(clean_rel_path),
        dest="output",
        help="Path to save cleaned and processed configs (default: %(default)s).",
        metavar="FILE",
        type=existing_file,
    )

    parser.add_argument(
        "-R", "--reverse",
        action="store_true",
        dest="reverse",
        help="Sort in descending order (only applies with --sort).",
    )

    parser.add_argument(
        "-S", "--sort",
        const="host,port",
        default=None,
        dest="sort",
        help=(
            "Sort entries by comma-separated fields. "
            "If used without value (e.g., '-S'), the default fields are '%(const)s'. "
            "If omitted, entries are not sorted."
        ),
        metavar="FIELDS",
        nargs="?",
        type=split_valid_params,
    )

    return parser.parse_args()


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


def save_configs(configs: list[dict[str, Any]], \
    path_configs_clean: str = "v2ray-configs-clean.txt", mode: str = "w") -> None:
    print(f"[SAVE] Saving configs...")
    with open(path_configs_clean, mode, encoding="utf-8") as file:
        file.writelines(f"{config.get('url', '')}\n" for config in configs)
    print(f"[SAVE] Saved {len(configs)} configs in '{path_configs_clean}'.")


def sort_by_params(configs: list[dict[str, Any]], params: list[str], \
    reverse: bool = False) -> list[dict[str, Any]]:
    print(f"[SORT] Sorting {len(configs)} configs by keys: {params} ({reverse=})...")
    if not params:
        return configs

    def sort_param(config: dict[str, Any]) -> tuple[tuple[int, Any | None], ...]:
        return tuple(
            (0, value) if (value := config.get(param, None)) is not None else (1, None)
            for param in params
        )

    sorted_configs = sorted(configs, key=sort_param, reverse=reverse)
    print(
        f"[SORT] Sorting completed. {len(sorted_configs)} configs sorted successfully.", 
        end="\n\n",
    )
    return sorted_configs


def split_valid_params(params: str) -> list[str]:
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


def main() -> None:
    try:
        args = parse_args()
        configs = load_configs(path_configs_raw=args.input)
        configs = process_configs(configs=configs, args=args)
        save_configs(configs=configs, path_configs_clean=args.output)
    except KeyboardInterrupt:
        print(f"[ERROR] Exit from the program!")
    except Exception as exception:
        print(f"[ERROR] {exception}")


if __name__ == '__main__':
    main()
