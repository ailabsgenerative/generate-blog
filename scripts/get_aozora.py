import re
import requests

def download_aozora_txt(url: str) -> str:
    """青空文庫のtxtファイルをURLからダウンロード"""
    response = requests.get(url)
    response.encoding = 'shift_jis'  # 青空文庫のテキストはShift_JIS
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

# 使用例（老妓抄）
url = "https://www.aozora.gr.jp/cards/001257/files/59898_70731.txt"

raw_text = download_aozora_txt(url)
clean_text = extract_main_text(raw_text)

# 結果を表示
print(clean_text[:1000])  # 上位1000文字を表示
