# init_data.py
from scraper import PoeScraper
from database import PoeDatabase

def main():
    print("=== 開始資料更新流程 ===")
    
    # Initialize Database
    db = PoeDatabase()
    
    # Start Scraping
    scraper = PoeScraper(headless=True)
    
    try:
        # Catch Ascendency
        print("正在抓取昇華職業...")
        ascendancies = scraper.scrape_ascendancies()
        if ascendancies:
            db.save_ascendancies(ascendancies)
        else:
            print("警告：沒有抓到昇華職業資料。")

        # Catch Skill Gems and Tags
        print("正在抓取技能寶石 (這需要一點時間)...")
        gems = scraper.scrape_active_gems()
        if gems:
            db.save_gems(gems)
        else:
            print("警告：沒有抓到技能寶石資料。")
            
    finally:
        # Finish Messages
        scraper.close()
        db.close()
        print("=== 資料更新完成！請檢查 poe_builds.db 是否已建立 ===")

if __name__ == "__main__":
    main()