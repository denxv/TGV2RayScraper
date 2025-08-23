
# TGV2RayScraper

TGV2RayScraper is a Python project designed to collect Telegram channel data, extract V2Ray configurations, clean and normalize them, and maintain up-to-date channel information. It supports both synchronous and asynchronous scraping and includes tools for managing channel lists.

## Quick Start

Follow these steps to get started quickly:

1. **Clone the repository**  
```bash
git clone https://github.com/denxv/TGV2RayScraper.git
cd TGV2RayScraper
```

2. **Create and activate a virtual environment**

* On Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

* On Windows:

```bash
python -m venv venv
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

## Project Structure

* **channels/** – Directory for storing channel data

  * `current.json` – JSON file with up-to-date channel data
  * `urls.txt` – Text file containing URLs of Telegram channels

* **scripts/** – Directory for data processing scripts

  * `async_scraper.py` – Asynchronous script for collecting channel data
  * `scraper.py` – Synchronous script for collecting channel data
  * `update_channels.py` – Script for updating channel data
  * `v2ray_cleaner.py` – Script for cleaning and normalizing V2Ray configurations

* **v2ray/** – Directory for storing V2Ray configuration files

  * `configs-clean.txt` – Cleaned and normalized V2Ray configurations
  * `configs-raw.txt` – Raw V2Ray configurations

* **requirements.txt** – List of project dependencies

* **main.py** – Main script for running project operations

---

## Usage

### 1. Running the Scrapers

Collect Telegram channel data using either the asynchronous or synchronous scraper:

* **Asynchronous Scraper**
  Collects data from channels concurrently for faster processing (experimental):

  ```bash
  python scripts/async_scraper.py
  ```

* **Synchronous Scraper**
  Processes channels one by one (simpler, may be slower):

  ```bash
  python scripts/scraper.py
  ```

### 2. Updating Channels

To update the channel list or synchronize new data into the current JSON file:

```bash
python scripts/update_channels.py
```

This script:

* Reads the current channel list (`channels/current.json`)
* Merges new URLs from `channels/urls.txt`
* Saves the updated list back to `current.json`
* Creates a timestamped backup like `current-YYYYMMDD-HHMMSS.json`

### 3. Cleaning V2Ray Configurations

To process raw V2Ray configuration files and produce cleaned/normalized output:

```bash
python scripts/v2ray_cleaner.py
```

This script:

* Reads raw configs from `v2ray/configs-raw.txt`
* Applies regex-based filters and normalization
* Writes cleaned configs to `v2ray/configs-clean.txt`

### 4. Running the Entire Project via `main.py`

You can run all main operations (scraping, updating channels, cleaning V2Ray configs) through the `main.py` script:

```bash
python main.py
```

By default, `main.py` executes the following scripts in order:

1. `update_channels.py` – Updates the channel list by merging new URLs from `channels/urls.txt` into `channels/current.json`, creating a timestamped backup.
2. `async_scraper.py` – Collects Telegram channel data asynchronously.
3. `v2ray_cleaner.py` – Processes raw V2Ray configuration files and saves cleaned configurations to `v2ray/configs-clean.txt`.

This provides a one-step way to update channels, scrape data, and clean V2Ray configurations. Each script is run sequentially, and any errors will stop the execution.

---

## Notes

* Always run scrapers before updating channels.
* Use the V2Ray cleaner after scraping to normalize configurations.
* Scripts are provided **as-is**; use at your own risk.

---

## Disclaimer

This software is provided "as-is". The author is **not responsible** for any damage, data loss, or other consequences resulting from the use of this software.

**Important:** Intended for educational/personal use only. The author is not responsible for:

* Misuse, including spamming or overloading Telegram servers.
* Unauthorized data collection.
* Legal or financial consequences.

Use responsibly and comply with platform terms.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
