# locales.py

# 定義所有字串的字典
TRANSLATIONS = {
    "tw": {
        # --- 系統設定 ---
        "lang_code": "tw",  # 用於網址 https://poedb.tw/tw/...
        "app_title": "POE 流派產生器 v2.2 (TW)",
        
        # --- 封面選單 ---
        "menu_start": "開始抽籤",
        "menu_update": "更新資料庫",
        "menu_lang": "切換語言 (Switch to English)",
        "menu_credit": "關於作者",
        "menu_quit": "離開",
        
        # --- 關於視窗 ---
        "credit_title": "關於",
        "credit_content": "開發者: Terry Chang\n版本: 2.2\n\n獻給所有流亡者。\nPowered by Python, Selenium & POEDB.",
        
        # --- 更新視窗/狀態 ---
        "update_confirm_title": "確認更新",
        "update_confirm_msg": "更新資料庫會開啟瀏覽器爬取資料，需要一點時間。\n(切換語言後建議重新更新一次以獲取對應語言的資料)\n\n要繼續嗎？",
        "update_running": "正在更新資料庫... 請稍候",
        "update_success": "資料庫更新完成！",
        "update_fail": "更新失敗，請檢查網路或驅動程式。",
        
        # --- 主功能介面 ---
        "lbl_asc_title": "🛡️ 昇華職業抽選",
        "lbl_count": "抽取數量:",
        "btn_roll_asc": "🎲 抽取昇華",
        "lbl_gem_title": "💎 技能寶石抽選",
        "lbl_filter": "標籤:",
        "btn_include": "➕ 包含",
        "btn_exclude": "➖ 排除",
        "btn_clear": "清除條件",
        "col_rule": "規則",
        "col_tag": "標籤",
        "rule_include": "[+] 包含",
        "rule_exclude": "[-] 排除",
        "btn_roll_gem": "🎲 抽取技能組合",
        "btn_back": "⬅ 回主選單",
        "btn_roll_all": "⚡ 一鍵抽取 (全部)",
        "col_gem_name": "寶石名稱",
        "col_gem_tags": "標籤",
        "msg_no_data": "無資料 (請先更新資料庫)",
        "msg_ready": "準備就緒。",
        "msg_roll_success": "成功抽取 {count} 個技能。",
        "msg_roll_fail": "找不到符合條件的技能。",
        
        # --- 爬蟲 Log (print用) ---
        "log_start_scrape": "開始爬取... 目標語言: Traditional Chinese",
        "log_asc_done": "昇華職業抓取完成。",
        "log_gem_done": "技能寶石抓取完成。",
    },
    "us": {
        # --- System ---
        "lang_code": "us", # URL segment for https://poedb.tw/us/...
        "app_title": "POE Build Generator v2.2 (EN)",
        
        # --- Menu ---
        "menu_start": "Start Rolling",
        "menu_update": "Update Database",
        "menu_lang": "Language (切換至中文)",
        "menu_credit": "Credits",
        "menu_quit": "Exit",
        
        # --- Credits ---
        "credit_title": "Credits",
        "credit_content": "Developer: Terry Chang\nVersion: 2.2\n\nDedicated to all Exiles.\nPowered by Python, Selenium & POEDB.",
        
        # --- Update ---
        "update_confirm_title": "Confirm Update",
        "update_confirm_msg": "Updating the database will open a browser to scrape data.\n(It is recommended to update data after switching languages.)\n\nContinue?",
        "update_running": "Updating database... Please wait.",
        "update_success": "Database updated successfully!",
        "update_fail": "Update failed. Check network or driver.",
        
        # --- Main App ---
        "lbl_asc_title": "🛡️ Ascendancy",
        "lbl_count": "Count:",
        "btn_roll_asc": "🎲 Roll Ascendancy",
        "lbl_gem_title": "💎 Skill Gems",
        "lbl_filter": "Tag:",
        "btn_include": "➕ Include",
        "btn_exclude": "➖ Exclude",
        "btn_clear": "Clear",
        "col_rule": "Rule",
        "col_tag": "Tag",
        "rule_include": "[+] Inc",
        "rule_exclude": "[-] Exc",
        "btn_roll_gem": "🎲 Roll Skills",
        "btn_back": "⬅ Main Menu",
        "btn_roll_all": "⚡ Roll All",
        "col_gem_name": "Gem Name",
        "col_gem_tags": "Tags",
        "msg_no_data": "No Data (Please update DB)",
        "msg_ready": "Ready.",
        "msg_roll_success": "Successfully rolled {count} gems.",
        "msg_roll_fail": "No matching gems found.",
        
        # --- Scraper Log ---
        "log_start_scrape": "Starting scraper... Target Language: English",
        "log_asc_done": "Ascendancies scraped.",
        "log_gem_done": "Skill gems scraped.",
    }
}

# 預設語言
current_lang = "tw"

def get_text(key):
    """取得當前語言的字串"""
    return TRANSLATIONS[current_lang].get(key, key)

def set_lang(lang):
    """切換語言"""
    global current_lang
    if lang in TRANSLATIONS:
        current_lang = lang

def get_lang_code():
    """取得網址用的語言代碼 (tw/us)"""
    return TRANSLATIONS[current_lang]["lang_code"]