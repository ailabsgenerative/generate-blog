import requests
from bs4 import BeautifulSoup

# 青空文庫の作家一覧ページなどのURL
url = "https://www.aozora.gr.jp/"

# ウェブページの内容を取得
response = requests.get(url)
response.encoding = 'shift_jis'  # 青空文庫はShift_JIS

# HTMLを解析
soup = BeautifulSoup(response.text, 'html.parser')

# 小説ページへのリンクを抽出
# 例: 青空文庫の「作家別一覧」からリンクを取得
links = soup.find_all('a', href=True)

# 各リンクをフィルタリングして小説のURLを取得
novel_urls = []
for link in links:
    href = link['href']
    if href.startswith('/cards/'):  # 小説ページのURLは「/cards/」で始まる
        novel_urls.append("https://www.aozora.gr.jp" + href)

# 結果を表示
print("小説ページのURL:")
for url in novel_urls:
    print(url)
