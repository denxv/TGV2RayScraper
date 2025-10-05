# TGV2RayScraper

TGV2RayScraper is a Python project designed to collect Telegram channel data, extract V2Ray configurations, and process them by cleaning, normalizing, and deduplicating, while maintaining up-to-date channel information. It supports both synchronous and asynchronous scraping and includes tools for managing channel lists.

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

* **aiohttp** – asynchronous HTTP client
* **aiofiles** – asynchronous file operations
* **asteval** – safe evaluation of Python expressions (used for filtering configs)
* **lxml** – parsing and processing HTML/XML
* **requests** – synchronous HTTP client
* **tqdm** – progress bar for long-running tasks

Other dependencies are listed in [`requirements.txt`](requirements.txt).

---

## Project Structure

* **channels/** – stores channel data
  * `current.json` – JSON file with up-to-date channel data
  * `urls.txt` – text file with Telegram channel URLs

* **configs/** – directory containing proxy configuration files
  * `v2ray-clean.txt` – cleaned, normalized, filtered, and deduplicated proxy configurations
  * `v2ray-raw.txt` – raw proxy configurations collected from various sources

* **docs/** – documentation folder
  * **ru/** – Russian-language documentation
    * `LICENSE` – license file for the documentation
    * `README.md` – main documentation file in Russian

* **logs/** – directory for storing logs of operations and configuration processing

* **scripts/** – data processing scripts
  * `async_scraper.py` – asynchronously collects data from Telegram channels
  * `logger.py` – logging utility with colorized console output and microsecond timestamps, used across all scripts
  * `scraper.py` – synchronously collects data from Telegram channels
  * `update_channels.py` – updates the channel list
  * `v2ray_cleaner.py` – utility for processing V2Ray and proxy configs: cleaning, normalization, filtering, deduplication, and sorting

* **requirements.txt** – lists all Python libraries required to run the project

* **main.py** – main script to run all project operations, including channel updates, data scraping, and proxy config processing

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

### **1. Updating Channels**

```bash
python scripts/update_channels.py
```

You can also run the script with `-h` to see all available options:

```bash
python scripts/update_channels.py -h
```

**Options include:**

* `-C, --channels FILE` — Path to the input JSON file containing the list of channels (default: `channels/current.json`).
* `-U, --urls FILE` — Path to a text file containing new channel URLs (default: `channels/urls.txt`).

---

The script:

* Reads the current channel list (`channels/current.json`).
* Merges with new URLs from `channels/urls.txt`.
* Creates timestamped backups of both files.
* Saves the updated list back to `current.json` and `urls.txt`.

---

**Example usage:**

```bash
python scripts/update_channels.py -C channels/current.json -U channels/urls.txt
```

---

### **2. Running Scrapers**

#### **Asynchronous Scraper** (faster, experimental)

```bash
python scripts/async_scraper.py
```

You can run with `-h` to see all available options:

```bash
python scripts/async_scraper.py -h
```

**Options include:**

* `-C, --channels FILE` — Path to the input JSON file containing the list of channels (default: `channels/current.json`).
* `-E, --batch-extract N` — Number of messages processed in parallel to extract V2Ray configs (default: 20).
* `-R, --configs-raw FILE` — Path to the output file for saving scraped V2Ray configs (default: `configs/v2ray-raw.txt`).
* `-U, --batch-update N` — Maximum number of channels updated in parallel (default: 100).

---

**Example usage:**

```bash
python scripts/async_scraper.py -E 20 -U 100 -C channels/current.json -R configs/v2ray-raw.txt
```

---

#### **Synchronous Scraper** (simpler, slower)

```bash
python scripts/scraper.py
```

You can run with `-h` to see all available options:

```bash
python scripts/scraper.py -h
```

**Options include:**

* `-C, --channels FILE` — Path to the input JSON file containing the list of channels (default: `channels/current.json`).
* `-R, --configs-raw FILE` — Path to the output file for saving scraped V2Ray configs (default: `configs/v2ray-raw.txt`).

---

**Example usage:**

```bash
python scripts/scraper.py -C channels/current.json -R configs/v2ray-raw.txt
```

---

### **3. Cleaning V2Ray Configurations**

```bash
python scripts/v2ray_cleaner.py
```

You can also run the script with `-h` to see all available options:

```bash
python scripts/v2ray_cleaner.py -h
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
python scripts/v2ray_cleaner.py -I configs/v2ray-raw.txt -O configs/v2ray-clean.txt --filter "re_search(r'speedtest|google', host)" -D "host, port" -S "protocol, host, port" --reverse
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
