# TGV2RayScraper

TGV2RayScraper is a Python project designed for collecting data from Telegram channels, extracting and processing V2Ray configurations, including cleaning, normalizing, and deduplicating them. The project maintains up-to-date information about channels and includes tools for managing their lists. It provides asynchronous tools for data collection and synchronous tools for processing V2Ray configurations.

> The project runs on Python version 3.10 or higher.

For Russian version, see [README.md](docs/ru/README.md)

## Quick Start

### Clone the repository

Clones the project to your computer:

```bash
git clone https://github.com/denxv/TGV2RayScraper.git
```

Changes into the project directory:

```bash
cd TGV2RayScraper
```

---

### Working with the `uv` command

> All `uv` commands work the same on Linux, macOS, and Windows.

#### Creating a virtual environment

Creates and activates the virtual environment:

```bash
uv venv
```

#### Installing dependencies

Installs only the main dependencies for running the project:

```bash
uv sync --no-dev
```

Installs all dependencies, including dev packages for tests and development:

```bash
uv sync
```

#### Running the project

Runs the main project script:

```bash
uv run python main.py
```

Alternative way to run the project:

```bash
uv run main.py
```

> This will update the channel list, collect data, and clean V2Ray configurations in a single run.

#### Testing and linting (only for development)

Runs all project tests automatically:

```bash
uv run pytest
```

Checks type correctness in all files:

```bash
uv run mypy .
```

Checks code style and errors:

```bash
uv run ruff check .
```

---

### Working with the `pip` command

#### Creating a virtual environment

Creates a virtual environment for the project:

```bash
python -m venv venv
```

Activates the virtual environment on Linux/macOS:

```bash
source venv/bin/activate
```

Activates the virtual environment on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

> If PowerShell blocks script execution, temporarily allow it with:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```

> Then run `.\venv\Scripts\Activate.ps1` again.

#### Installing dependencies

Installs the required libraries for running the project:

```bash
pip install -r requirements.txt
```

Installs all dependencies, including dev packages for tests and development:

```bash
pip install -r requirements.txt -r requirements-dev.txt
```

#### Running the project

Runs the main project script:

```bash
python main.py
```

> This will update the channel list, collect data, and clean V2Ray configurations in a single run.

#### Testing and linting (only for development)

Runs all project tests automatically:

```bash
pytest
```

Checks type correctness in all files:

```bash
mypy .
```

Checks code style and errors:

```bash
ruff check .
```

## Dependencies

### Main Dependencies

The project requires the following Python libraries (works with Python ≥ 3.10):

* **aiofiles** – asynchronous file handling

* **asteval** - safe evaluation of Python expressions (used for filtering channels and configurations)

* **httpx** - modern HTTP client with support for both synchronous and asynchronous requests

* **lxml** – parsing and processing HTML/XML

* **tqdm** – progress bar for long-running operations

The full list of dependencies is available in [`requirements.txt`](requirements.txt).

### Development Dependencies (Dev-dependencies)

For development and testing of the project, additional tools are required:

* **freezegun** – time freezing in tests

* **mypy** – type checking

* **pytest** – testing framework

* **pytest-asyncio** – support for asynchronous tests in `pytest`

* **pytest-cov** – test coverage reporting

* **pytest-mock** – mocking in tests

* **ruff** – static code analysis and linting

All dev-dependencies are listed in [`requirements-dev.txt`](requirements-dev.txt).

## Project Structure

* **adapters/** - adapters for asynchronous data operations

  * `channel.py` - asynchronous operations with channels

  * `config.py` - asynchronous processing of configurations

  * `scraper.py` - asynchronous channel data scraper

* **channels/** - folder for storing channel and URL list files

  * `current.json` - main file with Telegram channel information

  * `urls.txt` - main file with Telegram channel links

  * backups of these files are also stored (e.g., `current-backup-<timestamp>.json`, `urls-backup-<timestamp>.txt`)

* **configs/** - folder for storing V2Ray configurations

  * `v2ray-clean.txt` - cleaned configurations

  * `v2ray-raw.txt` - raw configurations

* **core/** - core utilities and constants

  * **constants/** - common constants, formats, messages, regex patterns, and string templates

    * `common.py` - core constants, default paths, script settings, channel/message parameters, timeouts, colors, flags

    * `formats.py` - date, time, log, and progress bar formats

    * `messages.py` - text messages for channels and errors

    * `patterns.py` - regular expressions for URLs, configs, and identifiers

    * `templates.py` - templates for logs, channels, configs, errors, files, and URLs

  * `decorators.py` - decorators (e.g., for logging)

  * `logger.py` - logging utility with colored console output and microsecond timestamps

  * `typing.py` - custom type aliases for the project (channels, V2Ray configs, CLI, sessions, etc.)

  * `utils.py` - utility and helper functions

* **docs/** - project documentation in multiple languages

  * `ru/` - Russian documentation

    * `README.md` - user guide in Russian

    * `LICENSE` - project license in Russian

* **domain/** - business logic and domain-specific functions

  * `channel.py` - operations with channels, sorting, filtering

  * `config.py` - processing and normalization of configurations

  * `predicates.py` - filtering logic and predicates

* **logs/** - folder for script logs

  * log files with timestamps (e.g., `2020-10-10.log`)

* **scripts/** - helper scripts for performing project tasks

  * `scraper.py` - script collects data from Telegram channels asynchronously

  * `update_channels.py` - script to update channels (removing inactive channels and adding new ones)

  * `v2ray_cleaner.py` - script cleans, normalizes, and processes obtained V2Ray configurations

* **tests/** - directory with all project tests, verifying correctness, stability, and module functionality

  * **e2e/** - end-to-end tests, verifying full system behavior under different usage scenarios (**not implemented**)

    * `test_async_scraper.py` - checks the asynchronous scraper with real data

    * `test_update_channels.py` - tests the process of updating channel information

    * `test_v2ray_cleaner.py` - verifies correct cleaning of V2Ray configurations

  * **fixtures/** - helper files and test data used across different tests (**not implemented**)

    * **channels/** - test data and lists for channel processing checks

      * `sample_current.json` - contains current channels for testing functions

      * `sample_urls.txt` - list of URLs for testing data loading

    * **configs/** - test configuration files for processing checks

      * `sample_v2ray_clean.txt` - contains cleaned configs for tests

      * `sample_v2ray_raw.txt` - contains raw, original configs for tests

  * **integration/** - integration tests, checking interaction between multiple modules (**not implemented**)

    * **async_/** - asynchronous integration scenarios to verify data flows

      * `test_async_channels_flow.py` - verifies correct processing of channels asynchronously

      * `test_async_configs_flow.py` - verifies correct processing of configs asynchronously

    * **sync/** - synchronous integration scenarios to verify data flows

      * `test_sync_channels_flow.py` - verifies correct processing of channels synchronously

      * `test_sync_configs_flow.py` - verifies correct processing of configs synchronously

  * **unit/** - unit tests, verifying individual functions and classes of the project

    * **adapters/** - adapter tests for data handling (**not implemented**)

      * `test_async_channel.py` - checks processing and validation of channels asynchronously

      * `test_async_config.py` - checks processing and validation of configs asynchronously

      * `test_async_scraper.py` - checks scraper locally asynchronously

    * **core/** - tests for core utilities and constants

      * **constants/** - constants and test data used for function verification

        * **examples/** - test data for function verification

          * `decorators.py` - test data for verifying decorator functionality

          * `logger.py` - test data for verifying logging and message output

          * `utils.py` - test data for verifying helper functions and utilities

        * **test_cases/** - pre-prepared test cases for parameterization

          * `decorators.py` - test cases for verifying decorators

          * `logger.py` - test cases for verifying logging

          * `utils.py` - test cases for verifying helper functions

        * `common.py` - local constants for core tests

      * `test_decorators.py` - verifies correctness of custom decorators

      * `test_logger.py` - verifies logging functionality and message formatting

      * `test_utils.py` - verifies helper utilities and functions

    * **domain/** - tests verifying the project's domain logic

      * **constants/** - domain constants, fixtures, and pre-prepared cases

        * **examples/** - test data for domain model verification

          * `channel.py` - examples of channels for logic verification

          * `config.py` - examples of configs for verification (**in progress**)

          * `predicates.py` - examples of predicates for filter verification

        * **fixtures/** - ready-to-use objects for tests

          * `channel.py` - ready channel objects for tests

          * `config.py` - ready config objects for tests (**in progress**)

        * **test_cases/** - ready test scenarios for parameterization

          * `channel.py` - test cases for channel logic verification

          * `config.py` - test cases for config logic verification (**in progress**)

          * `predicates.py` - test cases for predicate verification

        * `common.py` - local constants for domain logic tests

      * `test_channel.py` - verifies correctness of channel logic

      * `test_config.py` - verifies correctness of config logic (**in progress**)

      * `test_predicates.py` - verifies correctness of predicates

  * `conftest.py` - global pytest configuration, including fixtures and hooks for all tests

* **LICENSE** - project license (default in English)

* **main.py** - main script to run all project operations, including updating channels, collecting data, and processing configurations

* **pyproject.toml** - configuration file for project metadata, dependencies, and development tools (e.g., `mypy`, `ruff`, `pytest`), centralizing build and tooling settings

* **README.md** - main project documentation (default in English)

* **requirements-dev.txt** - list of development dependencies (testing, type checking, linters - `pytest`, `mypy`, `ruff`, etc.)

* **requirements.txt** - list of all required libraries for running the project

* **uv.lock** - dependency lock file, recording exact package versions for a reproducible environment

## Structure of Channel JSON File

The file `channels/current.json` contains information about Telegram channels. Each key is the **channel name**, and the value is an **object with the channel's metadata**.

### Example of Channel JSON

```json
{
    "channel_available": {
        "count": 5555,
        "current_id": 4444,
        "last_id": 4444,
        "state": 1
    },
    "channel_new_default": {
        "count": 0,
        "current_id": 1,
        "last_id": -1,
        "state": 0
    },
    "channel_will_be_deleted": {
        "count": 1234,
        "current_id": 5678,
        "last_id": -1,
        "state": -3
    },
    "channel_unavailable": {
        "count": 1000,
        "current_id": 3000,
        "last_id": -1,
        "state": -1
    }
}
```

### Detailed Description of Fields

* `count` - the number of V2Ray configurations found in the channel.

  * `0` - default value, the channel has not been processed yet or no configurations have been found.

  * `> 0` - the number of configurations found in an active channel.

    > The `count` value can grow indefinitely as new configurations appear in the channel.

* `current_id` - the ID of the current message from which scanning begins.

  * `1` - default value, scanning starts from the very beginning of the channel (old messages).

  * `< 0` - take the last `N` messages (new messages).

    > Example: if `last_id = 500` and `current_id = -100`, scanning goes from message `≥ 400` to the last message `≤ 500`.

* `last_id` - the ID of the last message in the channel.

  * `-1` - default value, the channel is temporarily or permanently unavailable.

  * `> 0` - the ID of the last available message.

    > Updated on each scan run.

* `state` - the channel status (active/undefined/inactive).

  * `1` - active channel when `last_id != -1`.

  * `0` - default value, status is not yet determined.

  * `-1` - inactive channel when `last_id == -1`.

    > If the channel is unavailable (`last_id == -1`), the `state` value decreases by 1 on each run, indicating the number of failed attempts to access the channel.

## Supported Protocols

The cleaned configuration file (`configs/v2ray-clean.txt`) contains entries in one of the following formats:

### **AnyTLS**

```text
anytls://password@host:port/path?params#name
anytls://password@host:port?params#name
```

### **Hy2 / Hysteria2**

```text
hy2://password@host:port/path?params#name
hy2://password@host:port?params#name
hysteria2://password@host:port/path?params#name
hysteria2://password@host:port?params#name
```

### **Shadowsocks / ShadowsocksR**

```text
ss://method:password@host:port#name
ss://method:password@host:port/path?params#name
ss://base64(method:password)@host:port#name
ss://base64(method:password)@host:port/path?params#name
ss://base64(method:password@host:port)#name
ssr://base64(host:port:protocol:method:obfs:base64(password)/?param=base64(value))
```

### **Trojan**

```text
trojan://password@host:port/path?params#name
trojan://password@host:port?params#name
```

### **TUIC**

```text
tuic://uuid:password@host:port/path?params#name
tuic://uuid:password@host:port?params#name
```

### **VLESS**

```text
vless://uuid@host:port/path?params#name
vless://uuid@host:port?params#name
```

### **VMess**

```text
vmess://base64(json)
vmess://uuid@host:port/path?params#name
vmess://uuid@host:port?params#name
```

### **WireGuard**

```text
wireguard://privatekey@host:port/path?params#name
wireguard://privatekey@host:port?params#name
```

## Usage

### **1. Update Channels**

You can run the channel update script as follows:

```bash
python -m scripts.update_channels
```

> You can also prepend `uv run` before any `python` command to run it through `uv`.

An alternative method using `PYTHONPATH` is also available:

```bash
PYTHONPATH=. python scripts/update_channels.py
```

You can use the `-h` flag to see all available options:

```bash
python -m scripts.update_channels -h
```

**Options**

* **Global options**

  * `--no-backup` - Skip creating backup files for channel and Telegram URL lists. By default, backup is created.

  * `--no-dry-run` - Disable check-only mode and actually assign `current_id`. By default, `dry-run` mode is enabled.

* **Input files**

  * `-C, --channels PATH` - Path to the JSON file containing the list of channels (default: `channels/current.json`).

  * `-U, --urls PATH` - Path to the input TXT file containing new channel URLs (default: `channels/urls.txt`).

* **Channel selection**

  * `-F, --channel-filter CONDITION` - Filter channels using a Python-like expression (for example: `count < 100 and current_id == last_id or state == -1`).

    > Used to select the channels to which reset operations (`--reset-*`) are applied.

* **Channel actions**

  * `-D, --delete-channels` - Delete channels that are unavailable or meet specific conditions. By default, deletion is disabled.

  * `-M, --message-offset N` - Number of recent messages taken into account when assigning `current_id`.

* **Channel reset options**

  * `--reset-all` - Reset all channel fields to their default values (can be combined with `--reset-<field>` and `--channel-filter`).

  * `--reset-count [N]` - Reset `count` to the specified value or to the default value (`0`).

  * `--reset-current-id [N]` - Reset `current_id` to the specified value or to the default value (`1`).

  * `--reset-last-id [N]` - Reset `last_id` to the specified value or to the default value (`-1`).

  * `--reset-state [N]` - Reset `state` to the specified value or to the default value (`0`).

**The script performs the following actions:**

* Loads the current list of channels from `channels/current.json`.

* Merges existing channels with new URLs from `channels/urls.txt`.

* Runs in dry-run mode by default without making any changes (can be disabled with `--no-dry-run`).

* Creates backup copies of the channel list and URL files if needed (backup can be disabled with `--no-backup`).

* Selects channels based on the specified filter (`--channel-filter`), if provided.

* Deletes unavailable or flagged channels when the `--delete-channels` option is used.

* Resets channel field values to their defaults or to explicitly specified values (`--reset-*`).

* Assigns or updates the `current_id` field, taking the specified message offset into account (`--message-offset`).

* Saves the updated data back to `channels/current.json` and `channels/urls.txt`.

* Logs detailed debug information and warnings for each processed channel.

**Example usage:**

```bash
python -m scripts.update_channels -C channels/current.json -U channels/urls.txt -F "count < 100" --no-dry-run --reset-all
```

> You can add `uv run` before the `python` command to run it via `uv`.

---

### **2. Running Scrapers**

#### **Asynchronous Scraper** (fast and stable)

You can run the asynchronous scraper as follows:

```bash
python -m scripts.scraper
```

> You can also prepend `uv run` before any `python` command to run it through `uv`.

An alternative method using `PYTHONPATH` is also available:

```bash
PYTHONPATH=. python scripts/scraper.py
```

You can use the `-h` flag to see all available options:

```bash
python -m scripts.scraper -h
```

**Options**

* **Input / Output files**

  * `-C, --channels PATH` - Path to the input JSON file containing the list of channels (default: `channels/current.json`).

  * `-R, --configs-raw PATH` - Path to the output TXT file for saving scraped V2Ray configs (default: `configs/v2ray-raw.txt`).

* **Processing / Parallelism**

  * `-E, --batch-extract N` - Number of messages processed in parallel when extracting V2Ray configurations (default: `20`).

  * `-U, --batch-update N` - Maximum number of channels updated in parallel (default: `100`).

* **Network / Timeout**

  * `-T, --time-out SECONDS` - HTTP client timeout in seconds for requests used while updating channel info and extracting V2Ray configurations (default: `30.0`).

**The script performs the following actions:**

* Loads the current list of channels from the file `channels/current.json`.

* Extracts V2Ray configurations in parallel, with the number of simultaneous requests set by `--batch-extract`.

* Updates channels in parallel, with the number of channels updated at the same time set by `--batch-update`.

* Uses an HTTP client with the `--time-out` for updating channels and extracting configurations.

* Saves the extracted V2Ray configurations to the file `configs/v2ray-raw.txt`.

* Logs detailed information about the extraction and update process, including errors and warnings for each channel.

**Example usage:**

```bash
python -m scripts.scraper -C channels/current.json -R configs/v2ray-raw.txt -E 20 -U 100 --time-out 30.0
```

> You can add `uv run` before the `python` command to run it through `uv`.

---

### **3. Cleaning V2Ray Configurations**

You can run the V2Ray configuration cleaner script as follows:

```bash
python -m scripts.v2ray_cleaner
```

> You can also prepend `uv run` before any `python` command to run it through `uv`.

Alternatively, you can run it using `PYTHONPATH`:

```bash
PYTHONPATH=. python scripts/v2ray_cleaner.py
```

You can also run with `-h` to see all available options:

```bash
python -m scripts.v2ray_cleaner -h
```

**Options**

* **Input files**

  * `-I, --configs-raw PATH` - Path to the input TXT file with raw V2Ray configs for parsing (default: `configs/v2ray-raw.txt`).

  * `--import [PATH]` - Path to the input JSON file with already parsed configs. If empty or invalid, raw configs will be parsed instead (default: `configs/v2ray.json`).

* **Output files**

  * `-O, --configs-clean PATH` - Path to the output TXT file for cleaned and processed configs (default: `configs/v2ray-clean.txt`).

  * `--export [PATH]` - Path to the output JSON file for exporting parsed configs for later reuse without re-parsing raw input (default: `configs/v2ray.json`).

* **Normalization options**

  * `-N, --no-normalize` - Disable normalization of configs. By default, normalization is enabled.

* **Filter / Sort**

  * `-D, --duplicate [FIELDS]` - Remove duplicates by specified fields (default: `protocol, host, port`).

  * `-F, --config-filter CONDITION` - Keep only entries matching a Python-like condition (e.g., `"host == '1.1.1.1' and port > 1000"`).

  * `-R, --reverse` - Sort in descending order (applies only with `--sort`).

  * `-S, --sort [FIELDS]` - Sort entries by comma-separated fields (default: `protocol`).

**The script performs the following:**

* Reads raw V2Ray configurations from the file `configs/v2ray-raw.txt` and parses them for further processing.

* Imports already parsed configurations from a JSON file using the `--import` option. If the specified file is empty or invalid, raw configs are parsed instead.

* Applies filters based on Python-like conditions using the `--config-filter` parameter and performs optional normalization, which can be disabled with `--no-normalize`.

* Removes duplicate entries based on specified fields when using the `--duplicate` option.

* Sorts entries by the specified fields using `--sort` and can reverse the order with `--reverse` if needed.

* Saves the cleaned and processed configurations to the file `configs/v2ray-clean.txt`.

* Exports parsed configurations to a JSON file using the `--export` option for later reuse without re-parsing the raw input.

* Supports flexible selection of fields for filtering, sorting, and removing duplicates, allowing extraction of only the required configurations.

* Logs detailed information about the processing, including errors and warnings for each configuration.

**Example usage:**

```bash
python -m scripts.v2ray_cleaner -I configs/v2ray-raw.txt -O configs/v2ray-clean.txt -F "re_search(r'speedtest|google', host)" --reverse -D "host, port" -S "protocol, host, port" --import configs/v2ray.json --export
```

> You can add `uv run` before the `python` command to run it through `uv`.

---

### **4. Running All Steps via `main.py`**

```bash
python main.py
```

> You can also prepend `uv run` before any `python` command to run it through `uv`.

You can also run with `-h` or `--help-scripts` to see all available options:

```bash
python main.py -h
```

```bash
python main.py --help-scripts
```

**Options include:**

* `-H, --help-scripts` - Display help information for all internal pipeline scripts.

**The script performs the following:**

* Executes all pipeline steps in order:

  1. `update_channels.py` – updates the list of channels.

  2. `scraper.py` – collects channel data from Telegram asynchronously.

  3. `v2ray_cleaner.py` – cleans, normalizes, and processes the scraped proxy configuration files.

* Collects only relevant arguments for each script automatically.

**Example usage:**

```bash
python main.py --batch-extract 10 --batch-update 100 --filter "host and port" --duplicate --sort "protocol" --reverse
```

> You can add `uv run` before the `python` command to run it through `uv`.

## Notes

* Always update the channel list before running the scrapers.

* Use the V2Ray cleaner after scraping to normalize configurations.

* Scripts are provided **as-is**; use at your own risk.

## Disclaimer

This software is provided "as-is". The author **is not responsible** for any damage, data loss, or other consequences resulting from the use of this software.

**Important:** Intended for educational/personal use only. The author is not responsible for:

* Misuse, including spamming or overloading Telegram servers

* Unauthorized data collection

* Any legal, financial, or other consequences

Use responsibly and comply with platform terms.

## License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.
