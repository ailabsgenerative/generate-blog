import re
import requests
from bs4 import BeautifulSoup

def get_txt_url_from_html_page(page_url: str) -> str:
    """作品ページのHTMLから .txt ファイルのURLを抽出"""
    response = requests.get(page_url)
    response.encoding = 'shift_jis'
    soup = BeautifulSoup(response.text, 'html.parser')

    link = soup.find('a', string='テキストファイル')
    if not link:
        raise ValueError("テキストファイルのリンクが見つかりません")

    href = link['href']
    return f"https://www.aozora.gr.jp{href}"

def download_aozora_txt(txt_url: str) -> str:
    """青空文庫のtxtファイルをURLからダウンロード"""
    response = requests.get(txt_url)
    response.encoding = 'shift_jis'
    return response.text

def extract_main_text(text: str) -> str:
    """本文部分のみを抽出し、整形する"""
    start_match = re.search(r'［＃ここから本文］', text)
    end_match = re.search(r'［＃ここで本文終わり］', text)

    if not start_match or not end_match:
        raise ValueError("本文のマーカーが見つかりません")

    main_text = text[start_match.end():end_match.start()]
    main_text = re.sub(r'《.*?》', '', main_text)
    main_text = re.sub(r'［＃.*?］', '', main_text)
    main_text = re.sub(r'｜', '', main_text)
    main_text = re.sub(r'\n\n+', '\n\n', main_text)

    return main_text.strip()

# 作品ページ（例：こころ）
page_url = "https://www.aozora.gr.jp/cards/000020/files/2569_28291.html"

# テキストURLを取得して本文を整形
txt_url = get_txt_url_from_html_page(page_url)
print(f"📄 テキストURL: {txt_url}")

raw_text = download_aozora_txt(txt_url)
clean_text = extract_main_text(raw_text)

# 上位1000文字を表示
print(clean_text[:1000])
