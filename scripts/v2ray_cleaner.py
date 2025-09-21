#!/usr/bin/env python
# coding: utf-8

import argparse
import json
import os
import re
import urllib.parse

# anytls://password@host:port/path?params#name
# anytls://password@host:port?params#name
ANYTLS_URL_PATTERN = re.compile(
    r'(?P<url>'
        r'(?P<protocol>anytls)://'
        r'(?P<password>(?:(?!://).)+)'
        r'@(?P<host>[^\s@]+)'
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
        r'@(?P<host>[^\s@]+)'
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
            r'@(?P<host>[^\s@]+)'
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
        r'(?P<host>[^\s]+)'
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
        r'@(?P<host>[^\s@]+)'
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
        r'@(?P<host>[^\s@]+)'
        r':(?P<port>\d{1,5})'
        r'(?P<path>/[^\s?#]*){0,1}'
        r'(?:\?(?P<params>(?:(?!://)[^\s#])*)){0,1}'
        r'(?:#(?P<name>[^\s/]*)){0,1}'
    r')'
)

# vless://password@host:port/path?params#name
# vless://password@host:port?params#name
VLESS_URL_PATTERN = re.compile(
    r'(?P<url>'
        r'(?P<protocol>vless\b)://'
        r'(?P<password>(?:(?!://).)+)'
        r'@(?P<host>[^\s@]+)'
        r':(?P<port>\d{1,5})'
        r'(?P<path>/[^\s?#]*){0,1}'
        r'(?:\?(?P<params>(?:(?!://)[^\s#])*)){0,1}'
        r'(?:#(?P<name>[^\s/]*)){0,1}'
    r')'
)

# vmess://base64(json)
# vmess://password@host:port/path?params#name
# vmess://password@host:port?params#name
VMESS_URL_PATTERN = re.compile(
    r'(?P<url>'
        r'(?P<protocol>vmess\b)://'
        r'(?:'
            r'(?P<password>(?:(?!://).)+)'
            r'@(?P<host>[^\s@]+)'
            r':(?P<port>\d{1,5})'
            r'(?P<path>/[^\s?#]*){0,1}'
            r'(?:\?(?P<params>(?:(?!://)[^\s#])*)){0,1}'
            r'(?:#(?P<name>[^\s/]*)){0,1}'
        r'|'
            r'(?P<base64>[\w+/]+={0,2})'
        r')'
    r')'
)

# wireguard://password@host:port/path?params#name
# wireguard://password@host:port?params#name
WIREGUARD_URL_PATTERN = re.compile(
    r'(?P<url>'
        r'(?P<protocol>wireguard\b)://'
        r'(?P<password>(?:(?!://).)+)'
        r'@(?P<host>[^\s@]+)'
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
    return os.path.abspath(os.path.join(os.path.dirname(__file__), path))


def existing_file(path: str) -> str:
    abs_path = os.path.abspath(path)
    if not os.path.isfile(abs_path):
        raise argparse.ArgumentTypeError(f"The file does not exist: {abs_path}")
    return abs_path


def parse_args() -> argparse.Namespace:
    raw_rel_path = "../v2ray/configs-raw.txt"
    clean_rel_path = "../v2ray/configs-clean.txt"

    parser = argparse.ArgumentParser(
        description="Clean and normalize V2Ray configs"
    )

    parser.add_argument(
        "-i", "--input",
        dest="input",
        type=existing_file,
        default=abs_path(raw_rel_path),
        help=f"Path to the raw V2Ray configs (default: {raw_rel_path})",
        metavar="FILE"
    )

    parser.add_argument(
        "-o", "--output",
        dest="output",
        type=existing_file,
        default=abs_path(clean_rel_path),
        help=f"Path to save cleaned V2Ray configs (default: {clean_rel_path})",
        metavar="FILE"
    )

    return parser.parse_args()


def main() -> None:
    try:
        args = parse_args()
        with open(args.input, "r", encoding="utf-8") as file:
            v2ray = urllib.parse.unquote(file.read())
        print(f"[LOAD] Loaded v2ray raw-configs from '{args.input}'!")

        with open(args.output, "w", encoding="utf-8") as file:
            for pattern in URL_PATTERNS:
                file.writelines([f"{config.groupdict(default='').get('url', '')}\n" \
                    for config in pattern.finditer(v2ray)])
        print(f"[SAVE] Saved v2ray clean-configs in '{args.output}'!")
    except Exception as exception:
        print(f"[ERROR] {exception}")


if __name__ == '__main__':
    main()
