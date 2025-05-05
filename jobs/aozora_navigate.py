import requests
from bs4 import BeautifulSoup
import time

def get_soup(url):
    """指定したURLからHTMLを取得し、BeautifulSoupオブジェクトを返す"""
    response = requests.get(url)
    response.raise_for_status()  # HTTPエラーがあれば例外を発生させる
    return BeautifulSoup(response.text, 'html.parser')

def navigate_aozora():
    base_url = "https://www.aozora.gr.jp/index_pages/"
    
    # 1. トップページから作家別のリンクを取得
    top_url = base_url + "index_top.html"
    print("1. トップページ:", top_url)
    soup = get_soup(top_url)
    
    # 作家別のリンクを取得（あいうえお順）
    author_links = soup.find_all('a', href=True)
    author_urls = [base_url + link['href'] for link in author_links if 'person' in link['href']]
    
    # 2. 「著作権存続になっていない」著者のページに入る
    for author_url in author_urls:
        if 'person_a.html' in author_url:  # 「著作権存続になっていない」著者ページ
            print("2. 著作権存続になっていない著者ページ:", author_url)
            soup = get_soup(author_url)
            
            # 3. 公開中の作品ページに入る
            works_link = soup.find('a', href=True, text="公開中の作品")
            if works_link:
                works_url = "https://www.aozora.gr.jp" + works_link['href']
                print("3. 公開中の作品ページ:", works_url)
                soup = get_soup(works_url)
                
                # 4. XHTMLファイルのHTMLリンクに入る
                xhtml_link = soup.find('a', href=True, text="XHTML")
                if xhtml_link:
                    xhtml_url = "https://www.aozora.gr.jp" + xhtml_link['href']
                    print("4. XHTMLファイルのHTMLリンク:", xhtml_url)
                    soup = get_soup(xhtml_url)
                    
                    # 5. 小説のページにたどり着く
                    novel_link = soup.find('a', href=True)
                    if novel_link:
                        novel_url = "https://www.aozora.gr.jp" + novel_link['href']
                        print("5. 小説のページ:", novel_url)
                        
                        # 次のリンクへ進む前に少し待機
                        time.sleep(2)

# スクリプトを実行
navigate_aozora()
