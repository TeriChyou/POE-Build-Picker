import sqlite3
import random

class PoeDatabase:
    def __init__(self, db_name="poe_builds.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ascendancies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS skill_gems (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                tags TEXT,
                link TEXT
            )
        ''')
        self.conn.commit()

    def save_ascendancies(self, ascendancy_list):
        for name in ascendancy_list:
            self.cursor.execute('INSERT OR IGNORE INTO ascendancies (name) VALUES (?)', (name,))
        self.conn.commit()

    def save_gems(self, gems_list):
        for gem in gems_list:
            self.cursor.execute('''
                INSERT OR REPLACE INTO skill_gems (name, tags, link)
                VALUES (?, ?, ?)
            ''', (gem['name'], gem['tags'], gem['link']))
        self.conn.commit()

    def get_all_tags(self):
        self.cursor.execute('SELECT tags FROM skill_gems')
        rows = self.cursor.fetchall()
        unique_tags = set()
        for row in rows:
            if row[0]:
                tags = [t.strip() for t in row[0].split(',')]
                unique_tags.update(tags)
        return sorted(list(unique_tags))

    def get_random_ascendancies(self, count=1):
        """
        隨機回傳指定數量的昇華職業
        """
        self.cursor.execute('SELECT name FROM ascendancies ORDER BY RANDOM() LIMIT ?', (count,))
        results = self.cursor.fetchall()
        # results 結構是 [('衛士',), ('死靈',)]，轉成 list
        return [r[0] for r in results] if results else []

    def get_random_gems(self, include_tags=None, exclude_tags=None, count=1):
        """
        隨機抽取指定數量的寶石
        """
        query = "SELECT name, tags, link FROM skill_gems WHERE 1=1"
        params = []

        if include_tags:
            for tag in include_tags:
                query += " AND tags LIKE ?"
                params.append(f'%{tag}%')

        if exclude_tags:
            for tag in exclude_tags:
                query += " AND tags NOT LIKE ?"
                params.append(f'%{tag}%')

        # 加上隨機排序與數量限制~~
        query += " ORDER BY RANDOM() LIMIT ?"
        params.append(count)

        self.cursor.execute(query, tuple(params))
        rows = self.cursor.fetchall()
        
        # 將結果包裝成字典列表回傳
        gems = []
        for r in rows:
            gems.append({
                "name": r[0],
                "tags": r[1],
                "link": r[2]
            })
        return gems

    def close(self):
        self.conn.close()