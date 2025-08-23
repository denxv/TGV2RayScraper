#!/usr/bin/env python
# coding: utf-8

import os
import sys
import subprocess

SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), 'scripts')


def run_script(script_name: str = "async_scraper.py") -> None:
    print('=' * 111)
    print(f"[INFO] Starting script '{script_name}'...")
    print('-' * 111)
    args = [sys.executable, os.path.join(SCRIPTS_DIR, script_name)]
    if subprocess.run(args=args).returncode:
        raise Exception(f"Script '{script_name}' exited with an error!")
    print('-' * 111)
    print(f"[INFO] Script '{script_name}' completed successfully!")


def main() -> None:
    scripts = [
        "update_channels.py",
        "async_scraper.py",
        "v2ray_cleaner.py",
    ]
    try:
        for script_name in scripts:
            run_script(script_name=script_name)
    except KeyboardInterrupt:
        print(f"[ERROR] Exit from the program!")
    except Exception as exception:
        print(f"[ERROR] {exception}")


if __name__ == "__main__":
    main()
