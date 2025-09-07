# TGV2RayScraper

TGV2RayScraper — это Python-проект, предназначенный для сбора данных с Telegram-каналов, извлечения V2Ray-конфигураций, их очистки и нормализации, а также для поддержания актуальной информации о каналах. Он поддерживает как синхронный, так и асинхронный сбор данных и включает инструменты для управления списками каналов.

Для английской версии смотрите [README.md](../../README.md)

---

## Быстрый старт

Следуйте этим шагам, чтобы быстро начать работу:

1. **Клонируем репозиторий**

```bash
git clone https://github.com/denxv/TGV2RayScraper.git
```

```bash
cd TGV2RayScraper
```

2. **Создаём и активируем виртуальное окружение**

* На Linux/macOS:

```bash
python -m venv venv
```

```bash
source venv/bin/activate
```

* На Windows:

```bash
python -m venv venv
```

```bash
venv\Scripts\activate
```

3. **Устанавливаем зависимости**

```bash
pip install -r requirements.txt
```

4. **Запускаем основной скрипт проекта**

```bash
python main.py
```

Это обновит список каналов, соберёт данные и очистит V2Ray-конфигурации за один запуск.

---

## Зависимости

Проект требует следующие библиотеки Python:

* **aiohttp** – асинхронный HTTP-клиент
* **aiofiles** – асинхронная работа с файлами
* **lxml** – парсинг и обработка HTML/XML
* **requests** – синхронный HTTP-клиент
* **tqdm** – индикатор прогресса для длительных операций

Другие зависимости перечислены в [`requirements.txt`](../../requirements.txt).

---

## Структура проекта

* **channels/** – хранение данных каналов

  * `current.json` – JSON-файл с актуальными данными о каналах
  * `urls.txt` – текстовый файл с URL-адресами Telegram-каналов

* **scripts/** – скрипты для обработки данных

  * `async_scraper.py` – асинхронный сбор данных с каналов
  * `scraper.py` – синхронный сбор данных с каналов
  * `update_channels.py` – обновление списка каналов
  * `v2ray_cleaner.py` – очистка и нормализация V2Ray-конфигураций

* **v2ray/** – хранение V2Ray-конфигураций

  * `configs-clean.txt` – очищенные и нормализованные конфигурации
  * `configs-raw.txt` – сырые конфигурации

* **requirements.txt** – список зависимостей проекта

* **main.py** – основной скрипт для запуска операций проекта

---

## Структура JSON каналов

Файл `channels/current.json` хранит метаданные о Telegram-каналах. Ключи верхнего уровня — это **имена каналов**, а значения — объекты с состоянием канала.

### Пример

```json
{
    "channel_name1": {
        "count": 0,
        "current_id": 1,
        "last_id": -1
    },
    "channel_name2": {
        "count": 0,
        "current_id": 1,
        "last_id": -1
    }
}
```

### Описание полей

* **`count`**

  * `> 0` → количество найденных V2Ray-конфигураций в активном канале (`count = 1`)
  * `= 0` → ничего не найдено или канал временно недоступен (`last_id = -1`)
  * `< 0` → количество неудачных попыток доступа к каналу

    * Каждая неудачная попытка уменьшает значение (`-1, -2, …`)
    * Когда `count <= -3`, канал считается неактивным и удаляется из `current.json` и `urls.txt`

* **`current_id`**

  * ID текущего сообщения, с которого начинается сканирование
  * `1` → сканирование начинается с самого начала канала
  * отрицательное → берутся последние N сообщений

    * Пример: если `last_id = 150` и `current_id = -100`, фактический `current_id` равен `150 - 100 = 50`. Сканирование начнётся с сообщения 50 и продвигается к последнему сообщению (`last_id = 150`).

* **`last_id`**

  * последний ID сообщения на канале
  * обновляется при каждом запуске
  * `-1` → канал временно или постоянно недоступен
  * в остальных случаях — положительное число

---

## Поддерживаемые протоколы

Файл очищенных конфигураций (`v2ray/configs-clean.txt`) содержит записи в одном из следующих форматов:

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
ss://base64(method:password)@host64:port64#name
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

## Использование

---

### **1. Обновление каналов**

```bash
python scripts/update_channels.py
```

---

Скрипт:

* Читает текущий список каналов (`channels/current.json`)
* Объединяет его с новыми URL-адресами из `channels/urls.txt`
* Создаёт резервные копии обоих файлов с меткой времени
* Сохраняет обновлённый список обратно в `current.json` и `urls.txt`

---

### **2. Запуск сканеров**

* **Асинхронный сканер** (быстрее, экспериментально)

```bash
python scripts/async_scraper.py
```

---

* **Синхронный сканер** (проще, медленнее)

```bash
python scripts/scraper.py
```

---

### **3. Очистка V2Ray-конфигураций**

```bash
python scripts/v2ray_cleaner.py
```

---

Скрипт:

* Читает сырые конфигурации из `v2ray/configs-raw.txt`
* Применяет фильтры на основе регулярных выражений и нормализацию
* Сохраняет очищенные конфигурации в `v2ray/configs-clean.txt`

---

### **4. Запуск всех операций через `main.py`**

```bash
python main.py
```

---

Выполняет скрипты в порядке:

1. `update_channels.py` – обновление списка каналов
2. `async_scraper.py` – асинхронный сбор данных с каналов
3. `v2ray_cleaner.py` – очистка и нормализация конфигураций

Обеспечивает одноступенчатый запуск обновления каналов, сбора данных и очистки конфигураций.

---

## Примечания

* Всегда обновляйте список каналов перед запуском сканеров.
* Используйте очистку V2Ray после сканирования для нормализации конфигураций.
* Скрипты предоставляются **как есть**; используйте их на свой страх и риск.

---

## Отказ от ответственности

Это программное обеспечение предоставляется «как есть». Автор **не несёт ответственности** за любой ущерб, потерю данных или другие последствия использования данного программного обеспечения.

**Важно:** предназначено только для образовательного/личного использования. Автор не отвечает за:

* Неправомерное использование, включая спам или перегрузку серверов Telegram
* Несанкционированный сбор данных
* Юридические или финансовые последствия

Используйте ответственно и соблюдайте правила платформы.

---

## Лицензия

Этот проект лицензирован под MIT License – см. файл [LICENSE](LICENSE) для деталей.
