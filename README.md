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

  * `--debug` - Enable debug logging in the console. By default, the console displays logs at `INFO` level.

  * `--no-dry-run` - Disable dry-run mode and allow modification of channel metadata, including assigning `current_id` and resetting fields (e.g. `count`, `last_id`, etc.). By default, dry-run mode is enabled.

  * `--skip-backup` - Skip creating backup files for channel and Telegram URL lists. By default, backup is created.

* **Input files**

  * `-C, --channels PATH` - Path to the JSON file containing the list of channels (default: `channels/current.json`).

  * `-U, --urls PATH` - Path to the input TXT file containing new channel URLs (default: `channels/urls.txt`).

* **Channel selection**

  * `-F, --channel-filter CONDITION` - Filter channels using a Python-like expression (for example: `"count < 100 and current_id == last_id or state == -1"`).

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

* Displays `INFO` level logs in the console by default, debug output can be enabled using the `--debug` option.

* Logs detailed debug information and warnings to the file `logs/yyyy-mm-dd.log`.

* Loads the current list of channels from `channels/current.json`.

* Merges existing channels with new URLs from `channels/urls.txt`.

* Runs in dry-run mode by default without making any changes (can be disabled with `--no-dry-run`).

* Creates backup files for channel and URL lists if necessary (backup creation can be skipped using `--skip-backup`).

* Selects channels based on the specified filter (`--channel-filter`), if provided.

* Deletes unavailable or flagged channels when the `--delete-channels` option is used.

* Resets channel field values to their defaults or to explicitly specified values (`--reset-*`).

* Assigns or updates the `current_id` field, taking the specified message offset into account (`--message-offset`).

* Saves the updated data back to `channels/current.json` and `channels/urls.txt`.

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

* **Global options**

  * `--debug` - Enable debug logging in the console. By default, the console displays logs at `INFO` level.

* **HTTP client**

  * `--proxy [URL]` - Proxy server for HTTP requests. Takes precedence over environment variables. If not specified, `HTTPS_PROXY`, `HTTP_PROXY`, and `ALL_PROXY` are used. If none are found, a local proxy is used by default (`socks5://127.0.0.1:10808`).

    * Supported protocols: `http`, `https`, `socks5`, `socks5h`.

    * Format: `protocol://[username:password@]host:port`.

  * `--retries N` - Maximum number of HTTP request retry attempts on failure (default: `3`).

  * `--retry-delay SECONDS` - Maximum number of HTTP request retry attempts after failed requests (default: `0.5`).

  * `--time-out SECONDS` - HTTP client timeout in seconds for requests used during channel information updates and V2Ray configuration extraction (default: `30.0`).

* **Input / Output files**

  * `-C, --channels PATH` - Path to the input JSON file containing the list of channels (default: `channels/current.json`).

  * `-R, --configs-raw PATH` - Path to the output TXT file for saving scraped V2Ray configurations (default: `configs/v2ray-raw.txt`).

* **Channel update pipeline**

  * `--skip-update` - Skip updating channel information. Avoids redundant requests if channels are already updated. By default, channel updates are performed.

  * `-U, --channels-batch N` - Number of channels processed per batch during updates (default: `100`).

* **Configuration extraction pipeline**

  * `-E, --configs-batch N` - Number of messages processed per batch during configuration extraction (default: `20`).

  * `-P, --channels-concurrency N` - Maximum number of channels processed concurrently during configuration extraction (default: `5`).

**The script performs the following actions:**

* Displays `INFO` level logs in the console by default, debug output can be enabled using the `--debug` option.

* Logs detailed information about the update and extraction process, including warnings and errors for each channel to the file `logs/yyyy-mm-dd.log`.

* Loads the current list of channels from `channels/current.json`.

* Updates channel metadata in parallel (unless `--skip-update` is specified), with the number of concurrently updated channels controlled by `--channels-batch`.

* Extracts V2Ray configurations in parallel using:

  * `--channels-concurrency` - the maximum number of channels processed simultaneously;

  * `--configs-batch` - the number of messages processed per step within a single channel.

* Routes all network requests through the proxy server specified via `--proxy`.

* Uses an HTTP client with timeout set by `--time-out` for all requests, including channel updates and configuration extraction.

* Uses retry logic on network failures (`--retries`) with delay between attempts (`--retry-delay`).

* Saves extracted V2Ray configurations to `configs/v2ray-raw.txt`.

**Example usage:**

```bash
python -m scripts.scraper -C channels/current.json -R configs/v2ray-raw.txt -E 20 -U 100 --proxy socks5://127.0.0.1:10808 --time-out 30.0 --skip-update
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

* **Global options**

  * `--debug` - Enable debug logging in the console. By default, the console displays logs at `INFO` level.

  * `--skip-normalize` - Skip config normalization to preserve their original structure. By default, normalization is enabled.

* **Input files**

  * `-I, --configs-raw PATH` - Path to the input TXT file with raw V2Ray configs for parsing (default: `configs/v2ray-raw.txt`).

  * `--import [PATH]` - Path to the input JSON file with already parsed configs. If empty or invalid, raw configs will be parsed instead (default: `configs/v2ray.json`).

* **Output files**

  * `-O, --configs-clean PATH` - Path to the output TXT file for cleaned and processed configs (default: `configs/v2ray-clean.txt`).

  * `--export [PATH]` - Path to the output JSON file for exporting parsed configs for later reuse without re-parsing raw input (default: `configs/v2ray.json`).

* **Filter / Sort**

  * `-D, --duplicate [FIELDS]` - Remove duplicates by specified fields (default: `"protocol, host, port"`).

  * `-F, --config-filter CONDITION` - Keep only entries matching a Python-like condition (e.g., `"host == '1.1.1.1' and port > 1000"`).

  * `-R, --reverse` - Sort in descending order (applies only with `--sort`).

  * `-S, --sort [FIELDS]` - Sort entries by comma-separated fields (default: `"protocol"`).

**The script performs the following:**

* Displays `INFO` level logs in the console by default, debug output can be enabled using the `--debug` option.

* Logs detailed information about the processing, including errors and warnings for each configuration to the file `logs/yyyy-mm-dd.log`.

* Reads raw V2Ray configurations from the file `configs/v2ray-raw.txt` and parses them for further processing.

* Imports already parsed configurations from a JSON file using the `--import` option. If the specified file is empty or invalid, raw configs are parsed instead.

* Applies filters based on Python-like conditions using the `--config-filter` parameter and performs optional normalization, which can be skipped via `--skip-normalize`.

* Removes duplicate entries based on specified fields when using the `--duplicate` option.

* Sorts entries by the specified fields using `--sort` and can reverse the order with `--reverse` if needed.

* Saves the cleaned and processed configurations to the file `configs/v2ray-clean.txt`.

* Exports parsed configurations to a JSON file using the `--export` option for later reuse without re-parsing the raw input.

* Supports flexible selection of fields for filtering, sorting, and removing duplicates, allowing extraction of only the required configurations.

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

You can also run with `-h` to see all available options:

```bash
python main.py -h
```

**Options**

* **Global options**

  * `-D, --debug` - Enable debug logging in the console. By default, the console displays logs at `INFO` level.

  * `-H, --help-scripts [NAMES]` - Show help for internal pipeline scripts. Script names can be provided as a comma-separated list (e.g. `"scraper, update_channels, v2ray_cleaner"`). If no value is provided (e.g. `-H`), help is shown for all scripts.

**The script performs the following:**

* Executes all pipeline steps in order:

  1. `update_channels.py` – updates the list of channels.

  2. `scraper.py` – collects channel data from Telegram asynchronously.

  3. `v2ray_cleaner.py` – cleans, normalizes, and processes the scraped proxy configuration files.

* Collects only relevant arguments for each script automatically.

**Example usage:**

```bash
python main.py --debug --configs-batch 10 --channels-batch 50 --channels-concurrency 10 --proxy --retry-delay 1.5 --channel-filter "state == -1" --config-filter "host and port" --duplicate --reset-all --reset-count 0 --reverse --sort "host, port"
```

> You can add `uv run` before the `python` command to run it through `uv`.

## Dependencies

### Main Dependencies

The project requires the following Python libraries (works with Python 3.10+):

* **aiofiles** – asynchronous file handling

* **asteval** – safe evaluation of Python expressions (used for filtering channels and configurations)

* **httpx[socks]** – modern HTTP client with async support and SOCKS proxy capabilities (includes `socksio` dependency)

* **lxml** – parsing and processing HTML/XML

* **rich** – enhanced terminal output, colored logging, and improved progress visualization

The full list of dependencies is available in [`requirements.txt`](requirements.txt).

### Development Dependencies (Dev-dependencies)

For development and testing of the project, additional tools are required:

* **mypy** – type checking

* **pytest** – testing framework

* **pytest-asyncio** – support for asynchronous tests in `pytest`

* **pytest-cov** – test coverage reporting

* **pytest-mock** – mocking in tests

* **ruff** – static code analysis and linting

All dev-dependencies are listed in [`requirements-dev.txt`](requirements-dev.txt).

## Project Structure

* **adapters/** - adapters for asynchronous work with external data and Telegram

  * `channel.py` - asynchronous HTTP requests to Telegram web previews, HTML parsing via `lxml`, extraction of post IDs, loading/saving JSON/URL and creating backups

  * `config.py` - asynchronous message extraction, V2Ray link parsing via regular expressions, progress bar management, config import/export to TXT/JSON

  * `scraper.py` - orchestrator for channel metadata updates: batching, concurrent processing, integration with `rich` renderers

* **channels/** - working storage for channel pool state

  * `current.json` - main JSON file with channel metadata (`count`, `current_id`, `last_id`, `state`)

  * `urls.txt` - source list of Telegram channel links to add to the pool

  * *automatic file backups are also stored here (e.g., `current-backup-<timestamp>.json`)*

* **configs/** - directory for collected and processed configurations

  * `v2ray-clean.txt` - final file with cleaned, normalized and filtered configurations

  * `v2ray-raw.txt` - raw configurations directly extracted by the scraper from posts

  * `v2ray.json` - JSON cache of parsed configurations to speed up repeated processing

* **core/** - project core: utilities, constants, types and infrastructure

  * **constants/** - static data, patterns, string templates and configuration limits

    * **messages/** - text constants for logging, split by levels

      * `error.py` - error messages

      * `info.py` - informational messages

      * `warning.py` - warnings

    * **patterns/** - compiled regular expressions

      * **v2ray/** - patterns for parsing URL formats of protocols

        * `common.py` - common V2Ray patterns (e.g., JSON detector)

        * `detector.py` - universal pattern for determining protocol and link body

        * `registry.py` - registry of patterns grouped by protocol

        * `url.py` - specific patterns for parsing fields of each protocol

      * `common.py` - patterns for config fields and parameter delimiters

      * `proxy.py` - validation of proxy server URLs

      * `telegram.py` - extraction of channel names from `t.me` links

    * **templates/** - string templates with variable interpolation for logs

      * **debug/** - debug message templates, organized by domain

        * `channel.py` - debug logs for channel operations

        * `common.py` - general debug logs not tied to a specific domain

        * `config.py` - debug logs for config operations

      * **info/** - informational message templates, organized by domain

        * `channel.py` - informational logs for channel operations

        * `common.py` - general informational logs

        * `config.py` - informational logs for config operations

      * `common.py` - general templates (e.g., progress bar description)

      * `error.py` - error message templates

      * `title.py` - title templates for log objects

      * `warning.py` - warning templates

    * `common.py` - base constants: batch/concurrency limits, paths, timeouts, default channel values, XPath selectors, `rich` colors

    * `formats.py` - formats for dates, times, log file names, backups and URL assembly

  * **terminal/** - command-line interface components based on `rich`

    * `console.py` - global console with custom color theme for logging

    * `logger.py` - `logging` configuration: output to console and file with microseconds, object serialization, level switching

    * `progress.py` - progress bar management: task creation, updates, asynchronous removal

    * `renderers.py` - rendering of channel status tables and live updates via `rich.live`

    * `tables.py` - factories for creating structured tables with specified columns and styles

  * `context.py` - `dataclass` contexts: HTTP client, file paths, batch and concurrency parameters

  * `decorators.py` - `@status` decorator for logging function start/finish and tracking dictionary size changes

  * `typing.py` - strict type aliases (`ParamSpec`, `Protocol`, `TypeAlias`, `TypedDict`) for the entire codebase

  * `utils.py` - general-purpose utilities: paths, base64, batching, CLI validation, number conversion, backups, safe regex

* **docs/** - localized documentation

  * **ru/** - Russian-language documentation

    * `README.md` - user guide in Russian

    * `LICENSE` - MIT license text in Russian

* **domain/** - business logic and domain functions

  * `channel.py` - channel logic: filtering, sorting, field reset, deletion, diff calculation, updating `current_id`/`last_id`/`state`, dry-run logic

  * `config.py` - config logic: normalization (base64 decoding for SS/SSR/VMess), filtering via `asteval`, deduplication by fields, sorting

  * `predicates.py` - predicates and conditions: checking channel availability/freshness, safe execution of Python expressions via `asteval.Interpreter`

* **logs/** - automatically created script execution logs

  * *log files with timestamps (e.g., `2020-10-20.log`)*

* **scripts/** - CLI scripts for executing main project tasks

  * `scraper.py` - launch asynchronous scraping: channel updates, config extraction, proxy/timeout/retry configuration

  * `update_channels.py` - pool management: merging with `urls.txt`, filtering, field reset, removing inactive channels, assigning `current_id`

  * `v2ray_cleaner.py` - post-processing: normalization, filtering, duplicate removal, sorting, result export

* **tests/** - catalog with all project tests, checking correctness, stability and module functionality

  * **e2e/** - end-to-end tests checking full system behavior (**not implemented**)

    * `test_async_scraper.py` - tests asynchronous scraper operation with real data

    * `test_update_channels.py` - tests the channel information update process

    * `test_v2ray_cleaner.py` - tests correctness of V2Ray configuration cleaning

  * **fixtures/** - auxiliary files and test data used for various tests (**not added**)

    * **channels/** - test data and lists for checking channel functionality

      * `sample_current.json` - contains current channels for testing functions

      * `sample_urls.txt` - list of URLs for testing data loading

    * **configs/** - test configuration files for checking processing

      * `sample_v2ray_clean.txt` - contains cleaned configs for tests

      * `sample_v2ray_raw.txt` - contains original, raw configs for tests

  * **integration/** - integration tests checking interaction between multiple modules (**not implemented**)

    * **async_/** - asynchronous integration scenarios for checking data flows

      * `test_async_channels_flow.py` - checks correctness of asynchronous channel processing

      * `test_async_configs_flow.py` - checks correctness of asynchronous config processing

    * **sync/** - synchronous integration scenarios for checking data flows

      * `test_sync_channels_flow.py` - checks correctness of synchronous channel processing

      * `test_sync_configs_flow.py` - checks correctness of synchronous config processing

  * **unit/** - unit tests checking individual functions and classes of the project

    * **adapters/** - adapter tests for data processing (**not implemented**)

      * `test_async_channel.py` - checks asynchronous channel processing and validation

      * `test_async_config.py` - checks asynchronous config processing and validation

      * `test_async_scraper.py` - checks scraper operation locally and asynchronously

    * **core/** - tests checking main utilities and constants

      * **constants/** - stores data for checking the core

        * **examples/** - collects raw examples for tests

          * **patterns/** - stores strings for checking expressions

            * **v2ray/** - prepares examples for checking protocols

              * `common.py` - stores JSON format string examples

              * `detector.py` - contains links for checking the detector

              * `registry.py` - provides data for registry testing

              * `url.py` - stores ready links for parsing

            * `telegram.py` - collects links for checking channels

          * **terminal/** - prepares data for checking the console

            * `logger.py` - contains strings for checking logs

          * `decorators.py` - collects examples for checking decorators

          * `utils.py` - stores data for checking utilities

        * **patterns/** - runs direct tests of regular expressions

          * **v2ray/** - checks ready protocol patterns

            * `test_common.py` - tests common JSON format rules

            * `test_detector.py` - checks protocol detection rules

            * `test_regitry.py` - checks registry operation correctness

            * `test_url.py` - tests URL parsing correctness

          * `test_telegram.py` - checks channel search correctness

        * **test_cases/** - forms ready parameters for tests

          * **patterns/** - prepares data sets for patterns

            * **v2ray/** - creates cases for checking protocols

              * `common.py` - forms parameters for JSON testing

              * `detector.py` - creates cases for detector checking

              * `registry.py` - prepares data for registry testing

              * `url.py` - prepares arguments for URL checking

            * `telegram.py` - forms sets for channel checking

          * **terminal/** - creates cases for terminal checking

            * `logger.py` - prepares parameters for log checking

          * `decorators.py` - prepares data for decorator testing

          * `utils.py` - forms cases for utility checking

      * **terminal/** - tests for terminal interface components and data display

        * `test_console.py` - checks console configuration and operation

        * `test_logger.py` - checks logging in the terminal interface

        * `test_progress.py` - checks progress bar display and updates

        * `test_renderers.py` - checks terminal output rendering functions

        * `test_tables.py` - checks table creation and formatting

      * `test_context.py` - checks correctness of application execution contexts

      * `test_decorators.py` - checks correctness of custom decorators

      * `test_utils.py` - checks operation of auxiliary utilities and functions

    * **domain/** - tests checking project domain logic functionality

      * **constants/** - domain constants, fixtures and prepared cases

        * **examples/** - test data of domain model for checking logic

          * `channel.py` - channel examples for checking processing logic

          * `config.py` - config examples for checking processing (**in progress**)

          * `predicates.py` - predicate examples for checking filters

        * **fixtures/** - ready objects for reuse in tests

          * `channel.py` - ready channel objects for tests

          * `config.py` - ready config objects for tests (**in progress**)

        * **test_cases/** - ready test scenarios for parametrization

          * `channel.py` - test cases for checking channel logic

          * `config.py` - test cases for checking config logic (**in progress**)

          * `predicates.py` - test cases for checking predicates

        * `common.py` - local constants for domain logic tests

      * `test_channel.py` - checks correctness of channel logic operation

      * `test_config.py` - checks correctness of config logic operation (**in progress**)

      * `test_predicates.py` - checks correctness of predicate operation

  * `conftest.py` - common pytest configuration, including fixtures and hooks for all tests

* **LICENSE** - project license text (in English by default)

* **main.py** - main script for executing all project operations, including channel updates, data collection and configuration processing

* **pyproject.toml** - project configuration file containing metadata, dependencies and development tool settings (e.g., `mypy`, `ruff`, `pytest`), centralizes build and environment parameters

* **README.md** - main project documentation (in English by default)

* **requirements.txt** - list of all required libraries for running the project

* **requirements-dev.txt** - list of dependencies for development (testing, typing, linters - `pytest`, `mypy`, `ruff`, etc.)

* **uv.lock** - dependency lock file fixing exact package versions for reproducible environment

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
