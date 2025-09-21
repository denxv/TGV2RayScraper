# TGV2RayScraper

TGV2RayScraper is a Python project designed to collect Telegram channel data, extract V2Ray configurations, clean and normalize them, and maintain up-to-date channel information. It supports both synchronous and asynchronous scraping and includes tools for managing channel lists.

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

  * `async_scraper.py` – collects channel data asynchronously
  * `scraper.py` – collects channel data synchronously
  * `update_channels.py` – updates the channel list
  * `v2ray_cleaner.py` – cleans and normalizes V2Ray configurations

* **v2ray/** – stores V2Ray configuration files

  * `configs-clean.txt` – cleaned and normalized configs
  * `configs-raw.txt` – raw configs

* **requirements.txt** – project dependencies

* **main.py** – main script to run project operations

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

    * Each failed attempt decreases the value (`-1, -2, …`)
    * When `count <= -3`, the channel is considered inactive and removed from `current.json` and `urls.txt`

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
ssr://base64(host:port:protocol:method:obfs:base64(password))
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
vless://password@host:port/path?params#name
vless://password@host:port?params#name
```

---

### **VMess**

```text
vmess://base64(json)
vmess://password@host:port/path?params#name
vmess://password@host:port?params#name
```

---

### **WireGuard**

```text
wireguard://password@host:port/path?params#name
wireguard://password@host:port?params#name
```

---

## Usage

---

### **1. Updating Channels**

```bash
python scripts/update_channels.py
```

---

The script:

* Reads the current channel list (`channels/current.json`)
* Merges with new URLs from `channels/urls.txt`
* Creates timestamped backups of both files
* Saves the updated list back to `current.json` and `urls.txt`

---

### **2. Running Scrapers**

* **Asynchronous Scraper** (faster, experimental)

```bash
python scripts/async_scraper.py
```

---

* **Synchronous Scraper** (simpler, slower)

```bash
python scripts/scraper.py
```

---

### **3. Cleaning V2Ray Configurations**

```bash
python scripts/v2ray_cleaner.py
```

---

The script:

* Reads raw configs from `v2ray/configs-raw.txt`
* Applies regex-based filters and normalization
* Saves cleaned configs to `v2ray/configs-clean.txt`

---

### **4. Running All Steps via `main.py`**

```bash
python main.py
```

---

Executes scripts in order:

1. `update_channels.py` – update the channel list
2. `async_scraper.py` – collect Telegram channel data asynchronously
3. `v2ray_cleaner.py` – clean and normalize configurations

Provides a one-step way to update channels, scrape data, and clean configurations.

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
