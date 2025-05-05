import requests
from bs4 import BeautifulSoup

# 青空文庫のURL
url = "https://www.aozora.gr.jp/cards/000020/files/2569_28291.html"

# ウェブページの内容を取得
response = requests.get(url)
response.encoding = 'shift_jis'  # ページの文字コードを設定（青空文庫はShift_JISが多い）

# HTMLを解析
soup = BeautifulSoup(response.text, 'html.parser')

# タイトルを抽出
title = soup.find('h1').text.strip()

# 本文を抽出
# 本文は<div class="main_text">の中にあることが多い
main_text = soup.find('div', class_='main_text')

# 本文から不要なタグを除去してテキストを抽出
if main_text:
    body_text = main_text.get_text(separator="\n").strip()
else:
    body_text = "本文が見つかりませんでした。"

# 結果を表示
print(f"タイトル: {title}")
print(f"本文: {body_text[:500]}...")  # 本文の最初の500文字を表示
