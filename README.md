# Path of Exile Build Generator (POE 流派抽籤機)

這是一個基於 Python 的隨機選流派，能夠自動爬取 [POEDB](https://poedb.tw/) 的資料，並隨機抽取「昇華職業」與「技能寶石」組合，幫助流亡者們在賽季拓荒或尋找靈感時打破選擇困難症！

## 功能

* **自動爬蟲**：使用 Selenium 自動抓取最新的昇華職業與技能寶石資訊(每次開啟時)。
* **本地資料庫**：使用 SQLite 儲存資料，支援離線查詢。
* **彈性篩選**：
    * 支援「包含 (+)」與「排除 (-」標籤（例如：包含 `法術` 但排除 `圖騰`）。
    * 支援批量抽取（一次抽 5 個技能）。
* **一鍵查詢**：雙擊抽到的技能，即可直接開啟 POEDB 詳細頁面。

## 安裝與環境設定

本專案使用 Python 開發。

1.  **Clone 此專案**
    ```bash
    git clone https://github.com/TeriChyou/POE-Build-Picker.git
    cd 你clone的資料夾位置名稱
    ```

2.  **安裝依賴套件**
    建議使用虛擬環境 (Virtual Environment)。
    ```bash
    pip install -r requirements.txt
    ```
    *(注意：本專案主要依賴 `selenium`, `webdriver-manager` 以及 `tkinter` (通常內建))*

## 如何使用

### 執行 Python 原始碼

**第一步：初始化資料庫**
首次使用或需要更新資料時，請執行：
```bash
python init_data.py
```
這會啟動 Chrome (背景模式) 爬取資料並建立 poe_builds.db。

第二步：啟動主程式

```bash
python gui.py
```
啟動後即可開始抽籤。

## Pack.rar

有已經打包好現成的.exe檔案，可以單純下載Pack.rar
先執行UpdateData.exe之後再開啟主程式PoeBuildPicker.exe
請勿刪除icon.ico 不然會執行失敗，每次大改的時候記得更新技能
