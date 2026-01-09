# scraper.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import locales # 匯入剛剛寫好的字庫

class PoeScraper:
    def __init__(self, headless=False):
        self.options = Options()
        if headless:
            self.options.add_argument("--headless")
        self.options.add_argument("user-agent=Mozilla/5.0")
        
        # 取得當前語言代碼 (tw 或 us)
        self.lang_code = locales.get_lang_code()
        
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)
        self.wait = WebDriverWait(self.driver, 10)
        
        print(locales.get_text("log_start_scrape"))

    def scrape_ascendancies(self):
        # 動態網址：利用 f-string 插入 lang_code
        url = f"https://poedb.tw/{self.lang_code}/Ascendancy_class"
        print(f"Go to: {url}")
        self.driver.get(url)
        
        ascendancy_list = []
        try:
            selector = "div.flex-grow-1 figcaption a"
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
            
            for elem in elements:
                name = elem.text.strip()
                if name and name not in ascendancy_list:
                    ascendancy_list.append(name)
            
            print(locales.get_text("log_asc_done"))
            return ascendancy_list
        except Exception as e:
            print(f"Error: {e}")
            return []

    def scrape_active_gems(self):
        # 動態網址
        url = f"https://poedb.tw/{self.lang_code}/Skill_Gems" 
        print(f"Go to: {url}")
        self.driver.get(url)

        gems_data = []
        try:
            table_selector = "table.filters tbody tr"
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, table_selector)))
            rows = self.driver.find_elements(By.CSS_SELECTOR, table_selector)
            
            for row in rows: 
                try:
                    name_elem = row.find_element(By.CSS_SELECTOR, "td:nth-child(2) a")
                    gem_name = name_elem.text.strip()
                    gem_link = name_elem.get_attribute("href")
                    
                    tags_text = ""
                    try:
                        tags_elem = row.find_element(By.CSS_SELECTOR, ".gem_tags")
                        tags_text = tags_elem.text.strip()
                    except:
                        tags_text = row.get_attribute("data-tags")
                    
                    if gem_name:
                        gems_data.append({
                            "name": gem_name,
                            "tags": tags_text,
                            "link": gem_link
                        })
                except:
                    continue
            print(locales.get_text("log_gem_done"))
            return gems_data
        except Exception as e:
            print(f"Error: {e}")
            return []

    def close(self):
        self.driver.quit()