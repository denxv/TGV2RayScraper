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

* **scripts/** – data processing scripts

  * `async_scraper.py` – asynchronously collects data from Telegram channels
  * `scraper.py` – synchronously collects data from Telegram channels
  * `update_channels.py` – updates the channel list
  * `v2ray_cleaner.py` – utility for processing V2Ray and proxy configs: cleaning, normalization, filtering, deduplication, and sorting

* **v2ray/** – stores proxy configuration files

  * `configs-clean.txt` – cleaned, normalized, filtered, and deduplicated configs
  * `configs-raw.txt` – raw proxy configs collected from various sources

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

The cleaned configuration file (`v2ray/configs-clean.txt`) contains entries in one of the following formats:

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

* `-C, --channels FILE` — Path to the current channels JSON file (default: `channels/current.json`).
* `-U, --urls FILE` — Path to the text file containing new channel URLs (default: `channels/urls.txt`).

---

The script:

* Reads the current channel list (`channels/current.json`).
* Merges with new URLs from `channels/urls.txt`.
* Creates timestamped backups of both files.
* Saves the updated list back to `current.json` and `urls.txt`.

---

### **2. Running Scrapers**

* **Asynchronous Scraper** (faster, experimental)

```bash
python scripts/async_scraper.py
```

You can run with `-h` to see all available options:

```bash
python scripts/async_scraper.py -h
```

**Options include:**

* `-C, --channels FILE` — Path to the current channels JSON file (default: `channels/current.json`).
* `-E, --batch-extract N` — Number of concurrent pages to extract V2Ray configs from (default: 20).
* `-O, --output FILE` — Path to save scraped V2Ray configs (default: `v2ray/configs-raw.txt`).
* `-U, --batch-update N` — Max number of concurrent channels to update info for (default: 100).

---

* **Synchronous Scraper** (simpler, slower)

```bash
python scripts/scraper.py
```

You can run with `-h` to see all available options:

```bash
python scripts/scraper.py -h
```

**Options include:**

* `-C, --channels FILE` — Path to the current channels JSON file (default: `channels/current.json`).
* `-O, --output FILE` — Path to save scraped V2Ray configs (default: `v2ray/configs-raw.txt`).

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
* `-I, --input FILE` — Path to the file with raw configs (default: `v2ray/configs-raw.txt`).
* `-N, --no-normalize` — Disable normalization (enabled by default).
* `-O, --output FILE` — File path to save cleaned and processed configs (default: `v2ray/configs-clean.txt`).
* `-R, --reverse` — Sort entries in descending order (only applies with `--sort`).
* `-S, --sort [FIELDS]` — Sort entries by comma-separated fields. If used without value (e.g., `-S`), the default fields are `host,port`. If omitted, entries are not sorted.

---

The script:

* Reads raw configs from `v2ray/configs-raw.txt`.
* Applies regex-based filters and normalization.
* Removes duplicates (if `--duplicate` is used).
* Sorts entries (if `--sort` is used).
* Saves cleaned and processed configs to `v2ray/configs-clean.txt`.

---

**Example usage:**

```bash
python scripts/v2ray_cleaner.py --filter "host == '1.1.1.1'" --duplicate --sort
```

---

### **4. Running All Steps via `main.py`**

```bash
python main.py
```

---

Executes scripts in order:

1. `update_channels.py` – update the channel list
2. `async_scraper.py` – collects channel data asynchronously from Telegram
3. `v2ray_cleaner.py` – cleans, normalizes, and processes proxy configuration files

Enables updating channels, scraping data, and cleaning configurations in a single step.

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
