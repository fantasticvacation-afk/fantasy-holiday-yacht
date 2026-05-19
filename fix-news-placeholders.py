#!/usr/bin/env python3
"""
移除 news.html 中不存在的新闻卡片
只保留前 10 篇有详情页的新闻（news-001 到 news-010）
"""

import re
from pathlib import Path

BASE_DIR = Path(__file__).parent
news_file = BASE_DIR / "news.html"

print("📝 处理 news.html 占位符新闻卡片...")

content = news_file.read_text(encoding='utf-8')

# 查找所有新闻卡片
news_cards = re.findall(r'<div class="news-card[^>]*>.*?</div>\s*</div>', content, re.DOTALL)
print(f"找到 {len(news_cards)} 个新闻卡片")

# 提取每个卡片的链接
cards_to_remove = []
for i, card in enumerate(news_cards):
    link_match = re.search(r'href="(news-\d+\.html)"', card)
    if link_match:
        link = link_match.group(1)
        news_num = int(re.search(r'news-(\d+)', link).group(1))
        
        if news_num > 10:  # news-011 及以后
            cards_to_remove.append((news_num, card))
            print(f"  将移除: {link}")

print(f"\n需要移除 {len(cards_to_remove)} 个占位符卡片")

# 移除这些卡片
for num, card in sorted(cards_to_remove, key=lambda x: x[0], reverse=True):
    content = content.replace(card, '')

# 写回文件
news_file.write_text(content, encoding='utf-8')
print(f"\n✅ 已更新 news.html")
