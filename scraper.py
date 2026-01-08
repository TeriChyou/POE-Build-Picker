import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class PoeScraper:
    def __init__(self, headless=True):
        """
        初始化 Selenium WebDriver
        """
        self.options = Options()
        if headless:
            self.options.add_argument("--headless")
        # Agent
        self.options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        self.options.add_argument('--blink-settings=imagesEnabled=false')
        self.options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)
        self.wait = WebDriverWait(self.driver, 10)

    def scrape_ascendancies(self):
        """
        爬取所有昇華職業名稱 (排除基礎職業)
        """
        url = "https://poedb.tw/tw/Ascendancy_class"
        print(f"正在前往 {url} 抓取昇華職業...")
        self.driver.get(url)
        
        ascendancy_list = []
        try:
            # 避開左側的基礎職業 (如：遊俠、野蠻人)，只抓右側的昇華 (如：銳眼、勇士)
            selector = "div.flex-grow-1 figcaption a"
            
            # 等待元素載入
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
            
            for elem in elements:
                name = elem.text.strip()
                # 過濾掉空字串或重複的
                if name and name not in ascendancy_list:
                    ascendancy_list.append(name)
            
            print(f"成功抓取 {len(ascendancy_list)} 個昇華職業。")
            return ascendancy_list

        except Exception as e:
            print(f"抓取昇華職業時發生錯誤: {e}")
            return []
        
    def scrape_active_gems(self):
        """
        爬取主動技能寶石及其標籤
        """
        url = "https://poedb.tw/tw/Skill_Gems" 
        print(f"正在前往 {url} 抓取技能寶石...")
        self.driver.get(url)

        gems_data = []
        try:
            # 針對 table.filters 的 tbody 裡面的 tr
            table_selector = "table.filters tbody tr"
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, table_selector)))
            
            rows = self.driver.find_elements(By.CSS_SELECTOR, table_selector)
            
            # 如果要抓全部，請改成: for row in rows:
            for row in rows: 
                try:
                    # 抓取第二個 td (index 1) 裡面的 a 標籤作為名字
                    name_elem = row.find_element(By.CSS_SELECTOR, "td:nth-child(2) a")
                    gem_name = name_elem.text.strip()
                    gem_link = name_elem.get_attribute("href")

                    # 抓取標籤：優先抓取顯示在介面上的 .gem_tags
                    # 如果沒有顯示，嘗試抓取 tr 的 data-tags 屬性
                    tags_text = ""
                    try:
                        tags_elem = row.find_element(By.CSS_SELECTOR, ".gem_tags")
                        tags_text = tags_elem.text.strip() # 這會拿到 "攻擊, 範圍效果, 近戰"
                    except:
                        # 如果找不到 gem_tags class，嘗試拿 data-tags
                        tags_text = row.get_attribute("data-tags")
                    
                    if gem_name:
                        gems_data.append({
                            "name": gem_name,
                            "tags": tags_text,
                            "link": gem_link
                        })
                except Exception as row_err:
                    # 某些特殊的 row 格式不同可能導致錯誤，跳過該行
                    continue

            print(f"成功抓取 {len(gems_data)} 個技能寶石資料。")
            return gems_data

        except Exception as e:
            print(f"抓取技能寶石時發生錯誤: {e}")
            return []

    def close(self):
        self.driver.quit()

if __name__ == "__main__":
    scraper = PoeScraper(headless=True) # 測試穩定後可以用 headless=True 加快速度
    
    # 1. 測試昇華
    ascendancies = scraper.scrape_ascendancies()
    print(f"抓到的昇華 ({len(ascendancies)}):", ascendancies)
    
    # 2. 測試寶石
    gems = scraper.scrape_active_gems()
    print(f"抓到的寶石範例 (前3筆): {gems[:3]}")
    
    scraper.close()