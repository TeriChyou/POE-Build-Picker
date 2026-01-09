# gui.py
import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
import threading
import json
import os

from database import PoeDatabase
from scraper import PoeScraper
import locales

# 設定檔名稱
CONFIG_FILE = "config.json"

class PoeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.load_config()
        
        self.title(locales.get_text("app_title"))
        self.iconbitmap('icon.ico')  
        self.geometry("800x700")
        
        # 【修正重點 1：RWD 權重設定】
        # 告訴 Tkinter，第 0 列和第 0 行要佔據 100% 的權重 (跟著視窗縮放)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # 建立容器
        self.container = tk.Frame(self)
        # 這裡改成 grid 並設定 sticky="nsew" (北南東西都要貼齊，即填滿)
        self.container.grid(row=0, column=0, sticky="nsew")
        
        # 容器內部也要設定權重，讓裡面的 Page 可以填滿容器
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        self.db = PoeDatabase()
        
        self.frames = {}
        
        for F in (MainMenu, AppPage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            # 這裡一樣要 sticky="nsew"
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainMenu")

    def show_frame(self, page_name):
        """切換顯示頁面"""
        frame = self.frames[page_name]
        frame.update_text() # 切換時重新刷新文字 (確保語言變更生效)
        frame.tkraise() # 將該頁面推到最上層

    def change_language(self):
        """切換語言邏輯"""
        new_lang = "us" if locales.current_lang == "tw" else "tw"
        locales.set_lang(new_lang)
        
        # 更新視窗標題
        self.title(locales.get_text("app_title"))
        
        # 刷新所有頁面的文字
        for frame in self.frames.values():
            frame.update_text()
            
        self.save_config() # 儲存設定

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    config = json.load(f)
                    locales.set_lang(config.get("lang", "tw"))
            except:
                pass

    def save_config(self):
        with open(CONFIG_FILE, "w") as f:
            json.dump({"lang": locales.current_lang}, f)
            
    def run_update_task(self):
        """執行資料庫更新 (背景執行)"""
        if not messagebox.askyesno(locales.get_text("update_confirm_title"), locales.get_text("update_confirm_msg")):
            return
            
        loading = tk.Toplevel(self)
        loading.title("Updating...")
        # 稍微調整一下 loading 視窗的大小和位置
        loading.geometry(f"300x120+{self.winfo_x() + 250}+{self.winfo_y() + 250}")
        
        lbl_loading = tk.Label(loading, text=locales.get_text("update_running"), pady=20, font=("Arial", 10))
        lbl_loading.pack()
        
        loading.transient(self)
        loading.grab_set()
        self.update()

        def task():
            local_db = None
            scraper = None
            try:
                # 1. 先爬蟲 (還不要動資料庫)
                scraper = PoeScraper(headless=True)
                
                lbl_loading.config(text="Scraping Ascendancy...")
                asc_data = scraper.scrape_ascendancies()
                
                lbl_loading.config(text="Scraping Gems...")
                gem_data = scraper.scrape_active_gems()
                
                # 2. 爬蟲成功後，才開啟資料庫連線
                local_db = PoeDatabase() 
                
                # 【修正重點 2：清空舊資料】
                lbl_loading.config(text="Clearing old data...")
                local_db.clear_all_data() 
                
                # 3. 寫入新資料
                lbl_loading.config(text="Saving new data...")
                local_db.save_ascendancies(asc_data)
                local_db.save_gems(gem_data)
                
                loading.destroy()
                messagebox.showinfo("Success", locales.get_text("update_success"))
                
                # 4. 回主線程刷新介面
                self.after(0, lambda: self.frames["AppPage"].refresh_tags())
                
            except Exception as e:
                loading.destroy()
                print(f"Update Error: {e}")
                messagebox.showerror("Error", f"{locales.get_text('update_fail')}\n{e}")
            finally:
                if scraper: scraper.close()
                if local_db: local_db.close()

        threading.Thread(target=task, daemon=True).start()
    
    def on_closing(self):
        self.db.close()
        self.destroy()

# ==============================
# 封面選單 (Cover Page)
# ==============================
class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.bg_color = "#2b2b2b"
        self.configure(bg=self.bg_color)
        
        # 建立一個置中用的容器 (Center Frame)
        # expand=True 會讓它佔據所有剩餘空間，配合 pack 的預設置中特性
        self.center_frame = tk.Frame(self, bg=self.bg_color)
        self.center_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # 標題
        self.lbl_title = tk.Label(self.center_frame, font=("Microsoft JhengHei", 24, "bold"), bg=self.bg_color, fg="white")
        self.lbl_title.pack(pady=(0, 40), anchor="center") # anchor="center" 確保本身置中
        
        # 按鈕容器 (讓按鈕整齊排列)
        btn_container = tk.Frame(self.center_frame, bg=self.bg_color)
        btn_container.pack(anchor="center")
        
        btn_style = {"font": ("Arial", 14), "width": 25, "pady": 5}
        
        self.btn_start = tk.Button(btn_container, command=lambda: controller.show_frame("AppPage"), bg="#f0ad4e", **btn_style)
        self.btn_start.pack(pady=10)
        
        self.btn_update = tk.Button(btn_container, command=controller.run_update_task, bg="#5bc0de", **btn_style)
        self.btn_update.pack(pady=10)
        
        self.btn_lang = tk.Button(btn_container, command=controller.change_language, bg="#d9534f", fg="white", **btn_style)
        self.btn_lang.pack(pady=10)
        
        self.btn_credit = tk.Button(btn_container, command=self.show_credit, bg="#5cb85c", **btn_style)
        self.btn_credit.pack(pady=10)

        self.btn_quit = tk.Button(btn_container, command=controller.on_closing, bg="#777", fg="white", **btn_style)
        self.btn_quit.pack(pady=10)

    def update_text(self):
        """刷新文字"""
        self.lbl_title.config(text=locales.get_text("app_title"))
        self.btn_start.config(text=locales.get_text("menu_start"))
        self.btn_update.config(text=locales.get_text("menu_update"))
        self.btn_lang.config(text=locales.get_text("menu_lang"))
        self.btn_credit.config(text=locales.get_text("menu_credit"))
        self.btn_quit.config(text=locales.get_text("menu_quit"))

    def show_credit(self):
        messagebox.showinfo(locales.get_text("credit_title"), locales.get_text("credit_content"))
# ==============================
# 主功能頁面 (Main App)
# ==============================
# gui.py 中的 AppPage 類別

class AppPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.db = controller.db
        self.filter_rules = []
        
        self.setup_ui()
    
    def setup_ui(self):
        main_frame = tk.Frame(self, padx=10, pady=10)
        main_frame.pack(fill="both", expand=True)

        # 【修改重點 1：頂部控制列 (Header)】
        # 使用一個 Frame 來達成「左邊一個按鈕、右邊一個按鈕」的效果
        header_frame = tk.Frame(main_frame)
        header_frame.pack(fill="x", pady=(0, 10))

        # 回首頁按鈕 (靠左)
        self.btn_back = tk.Button(header_frame, command=lambda: self.controller.show_frame("MainMenu"))
        self.btn_back.pack(side=tk.LEFT)

        # 一鍵抽取按鈕 (靠右)
        # 這裡用了一個比較顯眼的顏色 (#8e44ad 紫色)
        self.btn_roll_all = tk.Button(header_frame, command=self.roll_all, 
                                      bg="#8e44ad", fg="white", font=("Arial", 10, "bold"))
        self.btn_roll_all.pack(side=tk.RIGHT)

        # --- 昇華區 ---
        self.asc_frame = tk.LabelFrame(main_frame, padx=10, pady=10)
        self.asc_frame.pack(fill="x", pady=(0, 10))
        
        f1 = tk.Frame(self.asc_frame)
        f1.pack(fill="x")
        self.lbl_asc_count = tk.Label(f1)
        self.lbl_asc_count.pack(side=tk.LEFT)
        self.asc_spin = tk.Spinbox(f1, from_=1, to=19, width=5)
        self.asc_spin.pack(side=tk.LEFT, padx=5)
        self.btn_asc_roll = tk.Button(f1, command=self.roll_ascendancy, bg="#f0ad4e", fg="white")
        self.btn_asc_roll.pack(side=tk.LEFT, padx=10)
        
        self.asc_result = tk.Text(self.asc_frame, height=2, state="disabled", bg="#fdfdfd")
        self.asc_result.pack(fill="x", pady=5)

        # --- 技能區 ---
        self.gem_frame = tk.LabelFrame(main_frame, padx=10, pady=10)
        self.gem_frame.pack(fill="both", expand=True)

        # 篩選
        f2 = tk.Frame(self.gem_frame)
        f2.pack(fill="x", pady=5)
        self.lbl_gem_filter = tk.Label(f2)
        self.lbl_gem_filter.pack(side=tk.LEFT)
        
        self.tag_combo = ttk.Combobox(f2, state="readonly", width=15)
        self.tag_combo.pack(side=tk.LEFT, padx=5)
        
        self.btn_inc = tk.Button(f2, command=lambda: self.add_filter("include"), bg="#dff0d8")
        self.btn_inc.pack(side=tk.LEFT)
        self.btn_exc = tk.Button(f2, command=lambda: self.add_filter("exclude"), bg="#f2dede")
        self.btn_exc.pack(side=tk.LEFT, padx=2)
        self.btn_clr = tk.Button(f2, command=self.clear_filters)
        self.btn_clr.pack(side=tk.LEFT, padx=10)

        # 規則表
        self.rule_tree = ttk.Treeview(self.gem_frame, columns=("Type", "Tag"), show="headings", height=3)
        self.rule_tree.column("Type", width=80, anchor="center")
        self.rule_tree.column("Tag", width=200)
        self.rule_tree.bind("<Double-1>", self.delete_filter_rule)
        self.rule_tree.pack(fill="x", pady=5)

        # 抽技能按鈕
        f3 = tk.Frame(self.gem_frame, pady=5)
        f3.pack(fill="x")
        self.lbl_gem_count = tk.Label(f3)
        self.lbl_gem_count.pack(side=tk.LEFT)
        self.gem_spin = tk.Spinbox(f3, from_=1, to=20, width=5)
        self.gem_spin.pack(side=tk.LEFT, padx=5)
        self.btn_gem_roll = tk.Button(f3, command=self.roll_gem, bg="#5bc0de", fg="white", font=("Arial", 11, "bold"))
        self.btn_gem_roll.pack(side=tk.LEFT, padx=10)

        # 結果表
        self.gem_tree = ttk.Treeview(self.gem_frame, columns=("Name", "Tags", "Link"), show="headings")
        self.gem_tree.column("Name", width=150, anchor="center")
        self.gem_tree.column("Tags", width=400, anchor="w")
        self.gem_tree.column("Link", width=0, stretch=False)
        self.gem_tree.bind("<Double-1>", self.on_gem_double_click)
        self.gem_tree.pack(fill="both", expand=True)

        self.lbl_status = tk.Label(self, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.lbl_status.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.refresh_tags()

    def refresh_tags(self):
        raw_tags = self.db.get_all_tags()
        self.all_tags = sorted(raw_tags) if raw_tags else []
        self.tag_combo['values'] = self.all_tags
        if self.all_tags:
            self.tag_combo.current(0)

    def update_text(self):
        """介面文字多語言刷新"""
        self.btn_back.config(text=locales.get_text("btn_back"))
        
        # 【修改重點 2：更新一鍵抽取按鈕的文字】
        self.btn_roll_all.config(text=locales.get_text("btn_roll_all"))
        
        self.asc_frame.config(text=locales.get_text("lbl_asc_title"))
        self.lbl_asc_count.config(text=locales.get_text("lbl_count"))
        self.btn_asc_roll.config(text=locales.get_text("btn_roll_asc"))
        
        self.gem_frame.config(text=locales.get_text("lbl_gem_title"))
        self.lbl_gem_filter.config(text=locales.get_text("lbl_filter"))
        self.btn_inc.config(text=locales.get_text("btn_include"))
        self.btn_exc.config(text=locales.get_text("btn_exclude"))
        self.btn_clr.config(text=locales.get_text("btn_clear"))
        
        self.rule_tree.heading("Type", text=locales.get_text("col_rule"))
        self.rule_tree.heading("Tag", text=locales.get_text("col_tag"))
        
        self.lbl_gem_count.config(text=locales.get_text("lbl_count"))
        self.btn_gem_roll.config(text=locales.get_text("btn_roll_gem"))
        
        self.gem_tree.heading("Name", text=locales.get_text("col_gem_name"))
        self.gem_tree.heading("Tags", text=locales.get_text("col_gem_tags"))
        
        self.lbl_status.config(text=locales.get_text("msg_ready"))
        self.update_rule_list()

    # --- 邏輯功能 ---
    
    # 【修改重點 3：新增一鍵抽取邏輯】
    def roll_all(self):
        """同時執行昇華抽取與技能抽取"""
        self.roll_ascendancy()
        self.roll_gem()
        # 更新狀態列，顯示綜合訊息
        asc_text = self.asc_result.get("1.0", "end-1c")
        if " / " in asc_text:
            asc_count = len(asc_text.split(" / "))
        else:
            asc_count = 1 if asc_text and asc_text != locales.get_text("msg_no_data") else 0
            
        gem_count = len(self.gem_tree.get_children())
        
        if asc_count > 0 or gem_count > 0:
            self.lbl_status.config(text=f"Combo Rolled! Ascendancy: {asc_count}, Gems: {gem_count}")
        else:
            self.lbl_status.config(text=locales.get_text("msg_no_data"))

    def add_filter(self, f_type):
        tag = self.tag_combo.get()
        if tag and not any(r['tag'] == tag for r in self.filter_rules):
            self.filter_rules.append({'tag': tag, 'type': f_type})
            self.update_rule_list()

    def delete_filter_rule(self, event):
        sel = self.rule_tree.selection()
        if sel:
            tag = self.rule_tree.item(sel)['values'][1]
            self.filter_rules = [r for r in self.filter_rules if r['tag'] != tag]
            self.update_rule_list()

    def clear_filters(self):
        self.filter_rules = []
        self.update_rule_list()

    def update_rule_list(self):
        for item in self.rule_tree.get_children():
            self.rule_tree.delete(item)
        for rule in self.filter_rules:
            disp_type = locales.get_text("rule_include") if rule['type'] == 'include' else locales.get_text("rule_exclude")
            self.rule_tree.insert("", "end", values=(disp_type, rule['tag']))

    def roll_ascendancy(self):
        count = int(self.asc_spin.get())
        results = self.db.get_random_ascendancies(count)
        self.asc_result.config(state="normal")
        self.asc_result.delete("1.0", tk.END)
        self.asc_result.insert("1.0", " / ".join(results) if results else locales.get_text("msg_no_data"))
        self.asc_result.config(state="disabled")

    def roll_gem(self):
        count = int(self.gem_spin.get())
        includes = [r['tag'] for r in self.filter_rules if r['type'] == 'include']
        excludes = [r['tag'] for r in self.filter_rules if r['type'] == 'exclude']
        
        gems = self.db.get_random_gems(includes, excludes, count)
        
        for item in self.gem_tree.get_children():
            self.gem_tree.delete(item)
            
        if gems:
            for gem in gems:
                self.gem_tree.insert("", "end", values=(gem['name'], gem['tags'], gem['link']))
            self.lbl_status.config(text=locales.get_text("msg_roll_success").format(count=len(gems)))
        else:
            self.lbl_status.config(text=locales.get_text("msg_roll_fail"))

    def on_gem_double_click(self, event):
        sel = self.gem_tree.selection()
        if sel:
            link = self.gem_tree.item(sel)['values'][2]
            if link: webbrowser.open(link)

if __name__ == "__main__":
    app = PoeApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()