# Path of Exile Build Picker (POE 流派抽籤機) v2.2

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)

這是一個專為流亡黯道 (Path of Exile) 玩家設計的輔助工具。能夠自動爬取 [POEDB](https://poedb.tw/) 的最新資料，並透過隨機演算法抽取「昇華職業」與「技能寶石」組合。

專治每個賽季拓荒前的**選擇困難症**，一鍵幫你決定這季玩什麼！

## v2.2 版本特色

* **多語言支援**：完整支援 **繁體中文 (TW)** 與 **English (US)** 介面與資料庫切換。
* **RWD 響應式介面**：視窗可自由縮放，版面自動調整，操作更舒適。
* **一鍵 Combo**：右上角新增「一鍵抽取」按鈕，同時骰出職業與技能組合。
* **自動爬蟲更新**：內建 Selenium 爬蟲，可隨時從選單更新最新的遊戲資料（支援新賽季）。
* **彈性篩選系統**：
    * 支援「包含 (+)」標籤（例如：一定要 `法術`）。
    * 支援「排除 (-)」標籤（例如：絕對不要 `圖騰`）。
    * 支援批量抽取（例如：一次顯示 5 個技能供選擇）。
* **本地資料庫**：使用 SQLite 儲存，更新後即可離線使用。

## 安裝與環境設定 (開發者模式)

如果你懂 Python 並希望執行原始碼或進行修改，請參考以下步驟：

1.  **Clone 此專案**
    ```bash
    git clone [https://github.com/TeriChyou/POE-Build-Picker.git](https://github.com/TeriChyou/POE-Build-Picker.git)
    cd POE-Build-Picker
    ```

2.  **安裝依賴套件**
    建議使用虛擬環境 (Virtual Environment)。
    ```bash
    pip install -r requirements.txt
    ```
    *(主要依賴：`selenium`, `webdriver-manager` 以及 `tkinter`)*

3.  **執行主程式**
    ```bash
    python gui.py
    ```
    *首次執行請在封面選單點選「更新資料庫 (Update Database)」以初始化資料。*

## 下載執行檔 (一般使用者)

如果你不想安裝 Python，可以直接下載打包好的 `.exe` 檔案。

1.  下載 **Pack.rar** (位於 Releases 頁面或提供的連結)。
2.  解壓縮至任意資料夾。
3.  **重要注意事項**：
    * 請確保 `icon.ico` 檔案與執行檔位於同一目錄，**請勿刪除**，否則程式會閃退。
    * 電腦需安裝 **Google Chrome** 瀏覽器（爬蟲依賴）。

### 操作步驟

1.  **(首次使用/改版時)** 先執行 `UpdateData.exe` 進行資料更新。
    * *過程會開啟一個背景瀏覽器視窗，請耐心等待直到出現成功訊息。*
2.  開啟主程式 `PoeBuildPicker.exe` (或 `PoeSpinner.exe`)。
3.  開始抽籤！

## 更新日誌

* **v2.2**: 新增多語言切換、RWD 介面、一鍵 Combo 抽取功能。
* **v2.0**: UI 全面翻新，新增標籤包含/排除篩選功能。
* **v1.0**: 基礎爬蟲與隨機抽取功能。

## License

本專案採用 [MIT License](LICENSE) 授權。

# Path of Exile Build Picker v2.2

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)

A utility tool designed for Path of Exile players. It automatically scrapes the latest data from [POEDB](https://poedb.tw/) and uses a random algorithm to generate "Ascendancy" and "Skill Gem" combinations.

Designed to cure "choice paralysis" before a new league starts—decide your build with just one click!

## v2.2 Features

* **Multi-language Support**: Full support for Traditional Chinese (TW) and English (US) interface and database switching.
* **Responsive Interface (RWD)**: Resizable window with an auto-adjusting layout for a better user experience.
* **One-Click Combo**: Added a "Roll All" button in the top-right corner to generate Ascendancy and Skill combinations simultaneously.
* **Auto-Crawler Update**: Built-in Selenium crawler to update the latest game data directly from the menu (supports new leagues).
* **Flexible Filtering System**:
    * Supports "Include (+)" tags (e.g., must contain `Spell`).
    * Supports "Exclude (-)" tags (e.g., must not contain `Totem`).
    * Supports Batch Rolling (e.g., display 5 skills at once).
* **Local Database**: Uses SQLite for storage, allowing offline use after the initial update.

## Installation & Setup (Developer Mode)

If you are familiar with Python and wish to run the source code or modify it, please follow these steps:

1.  **Clone this repository**
    ```bash
    git clone [https://github.com/TeriChyou/POE-Build-Picker.git](https://github.com/TeriChyou/POE-Build-Picker.git)
    cd POE-Build-Picker
    ```

2.  **Install Dependencies**
    It is recommended to use a Virtual Environment.
    ```bash
    pip install -r requirements.txt
    ```
    *(Main dependencies: `selenium`, `webdriver-manager`, and `tkinter`)*

3.  **Run the Main Application**
    ```bash
    python gui.py
    ```
    *For the first run, please click "Update Database" in the main menu to initialize the data.*

## Download Executable (General User)

If you do not want to install Python, you can download the packaged `.exe` file directly.

1.  Download **Pack.rar** (from the Releases page or provided link).
2.  Extract the files to any folder.
3.  **Important Notes**:
    * Ensure `icon.ico` is in the same directory as the executable. **Do not delete it**, otherwise the program will crash.
    * **Google Chrome** must be installed on your computer (required for the crawler).

### Usage Steps

1.  **(First use / After update)** Run `UpdateData.exe` to update the database.
    * *This process will open a background browser window; please wait patiently until the success message appears.*
2.  Open the main program `PoeBuildPicker.exe` (or `PoeSpinner.exe`).
3.  Start rolling!

## Changelog

* **v2.2**: Added multi-language switching, RWD interface, and One-Click Combo feature.
* **v2.0**: UI overhaul, added include/exclude tag filtering.
* **v1.0**: Basic crawler and randomizer functions.

## License

This project is licensed under the [MIT License](LICENSE).