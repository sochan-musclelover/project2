import requests
from bs4 import BeautifulSoup
import csv
import time

url = "https://ja.wiktionary.org/wiki/Category:日本語_名詞"
words = []
headers = {"User-Agent": "Mozilla/5.0 (compatible; IdeaBot/1.0)"}
max_words = 10000  # 最大取得単語数

while url and len(words) < max_words:
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.content, "html.parser")
    for li in soup.select(".mw-category li"):
        if len(words) >= max_words:
            break
        word = li.text.strip()
        # 各単語ページから意味を取得
        word_url = li.find('a')
        meaning = ''
        if word_url and word_url.has_attr('href'):
            detail_url = "https://ja.wiktionary.org" + word_url['href']
            try:
                detail_res = requests.get(detail_url, headers=headers)
                detail_soup = BeautifulSoup(detail_res.content, "html.parser")
                # 最初の意味（定義）を取得
                meaning_tag = detail_soup.find('ol')
                if meaning_tag:
                    meaning_li = meaning_tag.find('li')
                    if meaning_li:
                        meaning = meaning_li.text.strip().replace('\n', ' ')
            except Exception:
                meaning = ''
            time.sleep(1)  # 単語詳細ページも1秒待機
        words.append((word, meaning))
    # 次ページ
    next_link = soup.find("a", string="次のページ")
    url = "https://ja.wiktionary.org" + next_link["href"] if next_link else None
    time.sleep(1)  # 1秒待機（DDoS防止）

# CSV出力
# with open("tmp/wiktionary_nouns.csv", "w", encoding="utf-8", newline="") as f:
with open("tmp/wiktionary_nouns2.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["No.", "Word", "Meaning"])
    for i, (word, meaning) in enumerate(words, 1):
        writer.writerow([i, word, meaning])