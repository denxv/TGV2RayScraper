# TGV2RayScraper

TGV2RayScraper is a Python project designed for collecting data from Telegram channels, extracting and processing V2Ray configurations, including cleaning, normalizing, and deduplicating them. The project maintains up-to-date information about channels and includes tools for managing their lists. It provides both synchronous and asynchronous tools for data collection and V2Ray configuration processing.

For Russian version, see [README.md](docs/ru/README.md)

---

## Quick Start

Follow these steps to get started quickly:

1. **Clone the repository**

```bash
git clone https://github.com/denxv/TGV2RayScraper.git
```

```bash
cd TGV2RayScraper
```

2. **Create and activate a virtual environment**

* On Linux/macOS:

```bash
python -m venv venv
```

```bash
source venv/bin/activate
```

* On Windows:

```bash
python -m venv venv
```

```bash
venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Run the main project script**

```bash
python main.py
```

This will update channels, scrape data, and clean V2Ray configurations in one step.

---

## Requirements

The project requires the following Python libraries:

* **aiofiles** – asynchronous file operations
* **asteval** – safe evaluation of Python expressions (used for filtering configs)
* **httpx** – modern HTTP client supporting both synchronous and asynchronous requests
* **lxml** – parsing and processing HTML/XML
* **tqdm** – progress bar for long-running tasks

Other dependencies are listed in [`requirements.txt`](requirements.txt).

---

## Project Structure

* **adapters/** — adapters for synchronous and asynchronous data operations
  * **async_/** — asynchronous implementations of operations (channels, configs, scraping)
    * `channels.py` — asynchronous operations for channels
    * `configs.py` — asynchronous configuration handling
    * `scraper.py` — asynchronous scraper for data collection
  * **sync/** — synchronous implementations of operations
    * `channels.py` — synchronous operations for channels
    * `configs.py` — synchronous configuration handling
    * `scraper.py` — synchronous scraper for data collection

* **core/** — core utilities and constants
  * `constants.py` — constants, default paths, URL templates, regex patterns, and script flags
  * `decorators.py` — decorators (e.g., for logging)
  * `logger.py` — logging utility with colorized console output and microsecond timestamps
  * `typing.py` — custom type aliases for the project (channels, V2Ray configs, CLI, sessions, etc.)
  * `utils.py` — utility functions and helpers

* **domain/** — business logic and domain functions
  * `channel.py` — channel management, sorting, filtering
  * `config.py` — processing and normalization of configurations
  * `predicates.py` — filtering logic and predicates

* **main.py** — main script for running all project operations, including channel updates, data scraping, and configuration processing

* **requirements.txt** — list of all required Python libraries for the project

---

## Channel JSON Structure

The file `channels/current.json` stores metadata about Telegram channels. Top-level keys are **channel usernames**, and values are objects with channel state.

### Example

```json
{
    "channel_new_default": {
        "count": 0,
        "current_id": 1,
        "last_id": -1
    },
    "channel_is_not_live": {
        "count": -1,
        "current_id": 100,
        "last_id": -1
    },
    "channel_live": {
        "count": 500,
        "current_id": 100,
        "last_id": 100
    },
    "channel_will_be_deleted": {
        "count": -3,
        "current_id": 100,
        "last_id": -1
    }
}
```

### Field Description

* **`count`**
  * `> 0` → number of V2Ray configurations in an active channel (`count = 1`)
  * `= 0` → nothing found, or channel temporarily unavailable (`last_id = -1`)
  * `< 0` → number of failed attempts to access the channel
    * Each failed attempt decreases the value (`-1, -2, …`).
    * When `count <= -3`, the channel is considered inactive and removed from `current.json` and `urls.txt`.

* **`current_id`**
  * starting message ID for scraping
  * `1` → start from the beginning of the channel
  * negative → take the last N messages
    * Example: if `last_id = 150` and `current_id = -100`, the effective `current_id` is `150 - 100 = 50`. Scraping will start from message 50 and move toward the last message (`last_id = 150`).

* **`last_id`**
  * latest message ID in the channel
  * updated on each run
  * `-1` → channel temporarily or permanently unavailable
  * otherwise, a positive integer

---

## Supported Protocols

The cleaned configuration file (`configs/v2ray-clean.txt`) contains entries in one of the following formats:

---

### **AnyTLS**

```text
anytls://password@host:port/path?params#name
anytls://password@host:port?params#name
```

---

### **Hy2 / Hysteria2**

```text
hy2://password@host:port/path?params#name
hy2://password@host:port?params#name
hysteria2://password@host:port/path?params#name
hysteria2://password@host:port?params#name
```

---

### **Shadowsocks / ShadowsocksR**

```text
ss://base64(method:password)@host:port#name
ss://method:password@host:port#name
ss://base64(method:password@host:port)#name
ssr://base64(host:port:protocol:method:obfs:base64(password)/?param=base64(value))
```

---

### **Trojan**

```text
trojan://password@host:port/path?params#name
trojan://password@host:port?params#name
```

---

### **TUIC**

```text
tuic://uuid:password@host:port/path?params#name
tuic://uuid:password@host:port?params#name
```

---

### **VLESS**

```text
vless://uuid@host:port/path?params#name
vless://uuid@host:port?params#name
```

---

### **VMess**

```text
vmess://base64(json)
vmess://uuid@host:port/path?params#name
vmess://uuid@host:port?params#name
```

---

### **WireGuard**

```text
wireguard://privatekey@host:port/path?params#name
wireguard://privatekey@host:port?params#name
```

---

## Usage

---

### **1. Update Channels**

You can run the channel update script as follows:

```bash
python -m scripts.update_channels
```

An alternative method using `PYTHONPATH` is also available:

```bash
PYTHONPATH=. python scripts/update_channels.py
```

You can use the `-h` flag to see all available options:

```bash
python -m scripts.update_channels -h
```

**Options include:**

* `--no-dry-run` — Disable dry run and actually assign `current_id` (default: disabled).
* `-C, --channels FILE` — Path to the input JSON file containing the list of channels (default: `channels/current.json`).
* `-D, --delete-channels` — Delete channels that are unavailable or meet specific conditions (default: disabled).
* `-M, --message-offset N` — Number of recent messages to include when assigning `current_id`.
* `-N, --include-new` — Include new channels in processing.
* `-U, --urls FILE` — Path to a text file containing new channel URLs (default: `channels/urls.txt`).

---

The script:

* Loads the current list of channels from `channels/current.json`.
* Merges with new URLs from `channels/urls.txt`.
* By default, performs a dry run without making changes (`--no-dry-run` disables it).
* Allows assigning `current_id` to channels taking message offset into account (`--message-offset`).
* Can include new channels in processing (`--include-new`).
* Supports deletion of unavailable or flagged channels (`--delete-channels`).
* Creates timestamped backups of both files.
* Saves the updated list back to `current.json` and `urls.txt`.
* Logs detailed warnings and debug information for each channel.

---

**Example usage:**

```bash
python -m scripts.update_channels -C channels/current.json -U channels/urls.txt -D -M 50 -N --no-dry-run
```

---

### **2. Running Scrapers**

#### **Asynchronous Scraper** (faster, experimental)

You can run the asynchronous scraper as follows:

```bash
python -m scripts.async_scraper
```

An alternative method using `PYTHONPATH` is also available:

```bash
PYTHONPATH=. python scripts/async_scraper.py
```

You can use the `-h` flag to see all available options:

```bash
python -m scripts.async_scraper -h
```

**Options include:**

* `-C, --channels FILE` — Path to the input JSON file containing the list of channels (default: `channels/current.json`).
* `-E, --batch-extract N` — Number of messages processed in parallel to extract V2Ray configs (default: 20).
* `-R, --configs-raw FILE` — Path to the output file for saving scraped V2Ray configs (default: `configs/v2ray-raw.txt`).
* `-U, --batch-update N` — Maximum number of channels updated in parallel (default: 100).

---

**Example usage:**

```bash
python -m scripts.async_scraper -E 20 -U 100 -C channels/current.json -R configs/v2ray-raw.txt
```

---

#### **Synchronous Scraper** (simpler, slower)

You can run the synchronous scraper as follows:

```bash
python -m scripts.scraper
```

Alternatively, you can run it with `PYTHONPATH`:

```bash
PYTHONPATH=. python scripts/scraper.py
```

Use `-h` to see all available options:

```bash
python -m scripts.scraper -h
```

**Options include:**

* `-C, --channels FILE` — Path to the input JSON file containing the list of channels (default: `channels/current.json`).
* `-R, --configs-raw FILE` — Path to the output file for saving scraped V2Ray configs (default: `configs/v2ray-raw.txt`).

---

**Example usage:**

```bash
python -m scripts.scraper -C channels/current.json -R configs/v2ray-raw.txt
```

---

### **3. Cleaning V2Ray Configurations**

You can run the V2Ray configuration cleaner script as follows:

```bash
python -m scripts.v2ray_cleaner
```

Alternatively, you can run it using `PYTHONPATH`:

```bash
PYTHONPATH=. python scripts/v2ray_cleaner.py
```

You can also run with `-h` to see all available options:

```bash
python -m scripts.v2ray_cleaner -h
```

**Options include:**

* `-D, --duplicate [FIELDS]` — Remove duplicate entries by specified comma-separated fields. If used without value (e.g., `-D`), the default fields are `protocol,host,port`. If omitted, duplicates are not removed.
* `-F, --filter CONDITION` — Filter entries using a Python-like condition. Example: `"host == '1.1.1.1' and port > 1000"`. Only matching entries are kept.
* `-I, --configs-raw FILE` — Path to the input file with raw V2Ray configs (default: `configs/v2ray-raw.txt`).
* `-N, --no-normalize` — Disable normalization (enabled by default).
* `-O, --configs-clean FILE` — Path to the output file for cleaned and processed configs (default: `configs/v2ray-clean.txt`).
* `-R, --reverse` — Sort entries in descending order (only applies with `--sort`).
* `-S, --sort [FIELDS]` — Sort entries by comma-separated fields. If used without value (e.g., `-S`), the default fields are `host,port`. If omitted, entries are not sorted.

---

The script:

* Reads raw configs from `configs/v2ray-raw.txt`.
* Applies regex-based filters and normalization.
* Removes duplicates (if `--duplicate` is used).
* Sorts entries (if `--sort` is used).
* Saves cleaned and processed configs to `configs/v2ray-clean.txt`.

---

**Example usage:**

```bash
python -m scripts.v2ray_cleaner -I configs/v2ray-raw.txt -O configs/v2ray-clean.txt --filter "re_search(r'speedtest|google', host)" -D "host, port" -S "protocol, host, port" --reverse
```

---

### **4. Running All Steps via `main.py`**

```bash
python main.py
```

You can also run with `-h` or `--help-scripts` to see all available options:

```bash
python main.py -h
```

```bash
python main.py --help-scripts
```

**Options include:**

* `-H, --help-scripts` — Display help information for all internal pipeline scripts.
* `-N, --no-async` — Use slower but simpler synchronous scraping mode instead of the default asynchronous mode.

---

The script:

* Executes all pipeline steps in order:
  1. `update_channels.py` – updates the list of channels.
  2. `async_scraper.py` – collects channel data from Telegram asynchronously (faster, used by default).
  3. `scraper.py` – collects channel data synchronously if `--no-async` is used (slower, simpler).
  4. `v2ray_cleaner.py` – cleans, normalizes, and processes the scraped proxy configuration files.

* Collects only relevant arguments for each script automatically.

---

**Example usage:**

```bash
python main.py --batch-extract 10 --batch-update 100 --filter "host and port" --duplicate --sort "protocol" --reverse
```

---

## Notes

* Always update the channel list before running the scrapers.
* Use the V2Ray cleaner after scraping to normalize configurations.
* Scripts are provided **as-is**; use at your own risk.

---

## Disclaimer

This software is provided "as-is". The author **is not responsible** for any damage, data loss, or other consequences resulting from the use of this software.

**Important:** Intended for educational/personal use only. The author is not responsible for:

* Misuse, including spamming or overloading Telegram servers
* Unauthorized data collection
* Legal or financial consequences

Use responsibly and comply with platform terms.

---

## License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.
