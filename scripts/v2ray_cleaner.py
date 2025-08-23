#!/usr/bin/env python
# coding: utf-8

import json
import os
import re

# ss://base64(method:password)@host64:port64#name
# ss://method:password@host:port#name
# ss://base64(method:password@host:port)#name
pattern_ss = re.compile(
    r'(?P<url>(?P<protocol>\bss\b)://'
        r'(?:'
            r'(?P<method>[^\s:@#]+)'
            r':(?P<password>(?:(?!://).)+)(?![^@])'
        r'|'
            r'(?P<base64>[\w+/%]+={0,2})(?![^\s@#])'
        r')'
        r'(?:'
            r'@(?P<host>[^\s@]+)'
            r':(?P<port>\d{1,5})'
        r'){0,1}'
        r'(?=(?:[\s#]))(?!\?)'
        r'(?:#(?P<name>[^\s/]*)){0,1}'
    r')'
)

# ssr://base64(host:port:protocol:method:obfs:base64(password))
pattern_ssr = re.compile(
    r'(?P<url>'
        r'(?P<protocol>\bssr\b)://'
        r'(?P<base64>[\w+/-]+={0,2})'
        r'(?:#(?P<name>[^\s/]*)){0,1}'
    r')'
)

# trojan://password@host:port/path?params#name
# trojan://password@host:port?params#name
pattern_trojan = re.compile(
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

# vless://password@host:port/path?params#name
# vless://password@host:port?params#name
pattern_vless = re.compile(
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
pattern_vmess = re.compile(
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

list_patterns = [
    pattern_ss,
    pattern_ssr,
    pattern_trojan,
    pattern_vless,
    pattern_vmess,
]


def create_file(file_path: str, data: str = "") -> str:
    if not os.path.exists(file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(data)
    return file_path


def main(path_configs_raw: str = "v2ray-configs-raw.txt",
    path_configs_clean: str = "v2ray-configs-clean.txt") -> None:
    try:
        with open(create_file(path_configs_raw), "r", encoding="utf-8") as file:
            v2ray = file.read()
        print(f"[LOAD] Loaded v2ray raw-configs from '{path_configs_raw}'!")

        with open(path_configs_clean, "w", encoding="utf-8") as file:
            for pattern in list_patterns:
                file.writelines([f"{config.groupdict(default='').get('url', '')}\n" \
                    for config in pattern.finditer(v2ray)])
        print(f"[SAVE] Saved v2ray clean-configs in '{path_configs_clean}'!")
    except Exception as exception:
        print(f"[ERROR] {exception}")


if __name__ == '__main__':
    clean_txt = os.path.join(os.path.dirname(__file__), "../v2ray/configs-clean.txt")
    raw_txt = os.path.join(os.path.dirname(__file__), "../v2ray/configs-raw.txt")
    main(path_configs_raw=raw_txt, path_configs_clean=clean_txt)
