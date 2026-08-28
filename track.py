# 每天抓取 Google Play 竞品数据，追加写入 data.csv
import csv, os
from datetime import datetime, timezone
from google_play_scraper import app

# ====== 监控的竞品包名（就是 Google Play 链接里 id= 后面那串） ======
APPS = [
    "com.h8games.littlefarmstory",   # Little Farm Story
    "com.playrix.township",          # Township
    "com.vizorapps.klondike",        # Klondike Adventures
    "com.samfinaco.paradise",        # Paradise
    "com.supercell.hayday",          # Hay Day
]
COUNTRY = "us"   # 市场：us 美国 / jp 日本
LANG = "en"      # 语言

rows = []
for pkg in APPS:
    try:
        a = app(pkg, lang=LANG, country=COUNTRY)
        rows.append({
            "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "app": a.get("title"),         # 应用名（自动抓取）
            "score": a.get("score"),       # 当前评分
            "ratings": a.get("ratings"),   # 累计评分数
            "reviews": a.get("reviews"),   # 评论数
            "installs": a.get("installs"), # 安装量区间（如 100,000,000+）
            "version": a.get("version"),   # 当前版本号
            "genre": a.get("genre"),       # 分类
        })
    except Exception as e:
        print(f"抓取失败 {pkg}: {e}")

# 追加写入 CSV，第一次运行自动建表头
if rows:
    file_exists = os.path.exists("data.csv")
    with open("data.csv", "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        if not file_exists:
            w.writeheader()
        w.writerows(rows)

print(f"抓取完成：{len(rows)} 个 App")
