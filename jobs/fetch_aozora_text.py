import sys
import requests
from bs4 import BeautifulSoup
import re
import os

def sanitize_filename(filename):
    """
    ファイル名に使用できない文字を置き換える。
    """
    return re.sub(r'[\\/*?:"<>|]', '_', filename)

def fetch_aozora_text(url):
    # 青空文庫のURLから内容を取得
    response = requests.get(url)
    response.encoding = 'shift_jis'

    # HTMLを解析
    soup = BeautifulSoup(response.text, 'html.parser')

    # タイトルを抽出
    title = soup.find('h1').text.strip()
    sanitized_title = sanitize_filename(title)  # ファイル名として安全な文字列に変換

    # 本文を抽出
    main_text = soup.find('div', class_='main_text')
    if main_text:
        body_text = main_text.get_text(separator="\n").strip()
    else:
        body_text = "本文が見つかりませんでした。"

    # 保存先ディレクトリ
    output_dir = "aozora_data"

    # ディレクトリが存在しない場合は作成
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # データを保存
    file_path = os.path.join(output_dir, f"{sanitized_title}.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"タイトル: {title}\n\n")
        f.write(body_text)

    print(f"Generated post: {file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python fetch_aozora_text.py <URL>")
        sys.exit(1)

    url = sys.argv[1]
    fetch_aozora_text(url)