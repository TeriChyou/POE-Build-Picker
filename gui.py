import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
from database import PoeDatabase

class PoeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("POE 一代 流派產生器 v2.1")
        self.root.geometry("800x700")
        self.root.iconbitmap("icon.ico")

        self.db = PoeDatabase()
        raw_tags = self.db.get_all_tags()
        self.all_tags = sorted(raw_tags) if raw_tags else []
        self.filter_rules = [] 
        
        self.setup_ui()

    def setup_ui(self):
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill="both", expand=True)

        # ==============================
        # 1. 昇華職業區 (支援多抽)
        # ==============================
        asc_frame = tk.LabelFrame(main_frame, text=" 🛡️ 昇華職業抽選 ", font=("Arial", 12, "bold"), padx=10, pady=10)
        asc_frame.pack(fill="x", pady=(0, 10))

        # 控制列
        asc_ctrl_frame = tk.Frame(asc_frame)
        asc_ctrl_frame.pack(fill="x")
        
        tk.Label(asc_ctrl_frame, text="抽取數量:").pack(side=tk.LEFT)
        self.asc_count_spin = tk.Spinbox(asc_ctrl_frame, from_=1, to=19, width=5)
        self.asc_count_spin.pack(side=tk.LEFT, padx=5)
        
        tk.Button(asc_ctrl_frame, text="🎲 抽取昇華", command=self.roll_ascendancy, 
                  bg="#f0ad4e", fg="white").pack(side=tk.LEFT, padx=10)

        # 結果顯示 (文字框)
        self.asc_result_text = tk.Text(asc_frame, height=3, font=("Microsoft JhengHei", 12), bg="#fdfdfd")
        self.asc_result_text.pack(fill="x", pady=5)
        self.asc_result_text.insert("1.0", "等待抽取...")
        self.asc_result_text.config(state="disabled") # 禁止手動編輯

        # ==============================
        # 2. 技能寶石區 (支援多抽)
        # ==============================
        gem_frame = tk.LabelFrame(main_frame, text=" 💎 技能寶石抽選 ", font=("Arial", 12, "bold"), padx=10, pady=10)
        gem_frame.pack(fill="both", expand=True)

        # --- 篩選控制 ---
        filter_ctrl = tk.Frame(gem_frame)
        filter_ctrl.pack(fill="x", pady=5)

        tk.Label(filter_ctrl, text="標籤:").pack(side=tk.LEFT)
        self.tag_combobox = ttk.Combobox(filter_ctrl, values=self.all_tags, state="readonly", width=15)
        if self.all_tags: self.tag_combobox.current(0)
        self.tag_combobox.pack(side=tk.LEFT, padx=5)

        tk.Button(filter_ctrl, text="➕ 包含", command=lambda: self.add_filter("include"), bg="#dff0d8").pack(side=tk.LEFT)
        tk.Button(filter_ctrl, text="➖ 排除", command=lambda: self.add_filter("exclude"), bg="#f2dede").pack(side=tk.LEFT, padx=2)
        tk.Button(filter_ctrl, text="清除條件", command=self.clear_filters).pack(side=tk.LEFT, padx=10)

        # 規則顯示
        self.rule_tree = ttk.Treeview(gem_frame, columns=("Type", "Tag"), show="headings", height=3)
        self.rule_tree.heading("Type", text="規則")
        self.rule_tree.heading("Tag", text="標籤")
        self.rule_tree.column("Type", width=80, anchor="center")
        self.rule_tree.column("Tag", width=200)
        self.rule_tree.bind("<Double-1>", self.delete_filter_rule)
        self.rule_tree.pack(fill="x", pady=5)

        # --- 抽籤控制 ---
        roll_ctrl = tk.Frame(gem_frame, pady=10)
        roll_ctrl.pack(fill="x")

        tk.Label(roll_ctrl, text="抽取數量:").pack(side=tk.LEFT)
        self.gem_count_spin = tk.Spinbox(roll_ctrl, from_=1, to=20, width=5)
        self.gem_count_spin.pack(side=tk.LEFT, padx=5)

        tk.Button(roll_ctrl, text="🎲 抽取技能組合", command=self.roll_gem, 
                  bg="#5bc0de", fg="white", font=("Arial", 11, "bold")).pack(side=tk.LEFT, padx=10)
        
        tk.Label(roll_ctrl, text="(雙擊下方列表可開啟 POEDB 網頁)", fg="gray").pack(side=tk.LEFT, padx=10)

        # --- 結果顯示---
        # 這裡用 Treeview 來列出多個技能比較整齊
        columns = ("Name", "Tags", "Link")
        self.gem_tree = ttk.Treeview(gem_frame, columns=columns, show="headings")
        
        self.gem_tree.heading("Name", text="寶石名稱")
        self.gem_tree.heading("Tags", text="標籤")
        self.gem_tree.heading("Link", text="連結 (隱藏)")
        
        self.gem_tree.column("Name", width=150, anchor="center")
        self.gem_tree.column("Tags", width=400, anchor="w")
        self.gem_tree.column("Link", width=0, stretch=False) # 隱藏 Link 欄位，不顯示但存著用
        
        self.gem_tree.pack(fill="both", expand=True)
        
        # 綁定雙擊事件
        self.gem_tree.bind("<Double-1>", self.on_gem_double_click)

        # 底部狀態
        self.status_label = tk.Label(self.root, text="準備就緒。", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

    # --- 邏輯功能 ---

    def add_filter(self, filter_type):
        tag = self.tag_combobox.get()
        if not tag: return
        for rule in self.filter_rules:
            if rule['tag'] == tag: return
        self.filter_rules.append({'tag': tag, 'type': filter_type})
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
        for item in self.rule_tree.get_children(): self.rule_tree.delete(item)
        for rule in self.filter_rules:
            disp = "[+] 包含" if rule['type'] == 'include' else "[-] 排除"
            self.rule_tree.insert("", "end", values=(disp, rule['tag']))

    def roll_ascendancy(self):
        count = int(self.asc_count_spin.get())
        results = self.db.get_random_ascendancies(count)
        
        self.asc_result_text.config(state="normal")
        self.asc_result_text.delete("1.0", tk.END)
        if results:
            # 用逗號分隔顯示
            self.asc_result_text.insert("1.0", " / ".join(results))
        else:
            self.asc_result_text.insert("1.0", "無資料")
        self.asc_result_text.config(state="disabled")

    def roll_gem(self):
        count = int(self.gem_count_spin.get())
        includes = [r['tag'] for r in self.filter_rules if r['type'] == 'include']
        excludes = [r['tag'] for r in self.filter_rules if r['type'] == 'exclude']
        
        gems = self.db.get_random_gems(includes, excludes, count)
        
        # 清空舊結果
        for item in self.gem_tree.get_children():
            self.gem_tree.delete(item)
            
        if gems:
            for gem in gems:
                self.gem_tree.insert("", "end", values=(gem['name'], gem['tags'], gem['link']))
            self.status_label.config(text=f"成功抽取 {len(gems)} 個技能。")
        else:
            messagebox.showinfo("提示", "找不到符合條件的技能，請放寬篩選條件。")

    def on_gem_double_click(self, event):
        """雙擊列表開啟連結"""
        sel = self.gem_tree.selection()
        if sel:
            # 取得 hidden column (Link) 的值
            item = self.gem_tree.item(sel)
            link = item['values'][2] # Index 2 是 Link
            if link:
                webbrowser.open(link)

    def on_closing(self):
        self.db.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PoeApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()