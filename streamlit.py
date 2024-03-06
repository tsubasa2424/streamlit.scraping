import streamlit as st
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

def main():
    st.set_page_config(page_title="Web Scraper")

    st.title("Web Scraper")

    selected_bg_color = st.selectbox("背景色の選択:", ["#00FF00", "#A0A0A0", "#C0C0C0"])
    st.markdown(f'<style>body{{background-color: {selected_bg_color};}}</style>', unsafe_allow_html=True)

    url = st.text_input("URLを入力:")
    keyword = st.text_input("キーワードを入力:")

    if st.button("検索"):
        scrape_website(url, keyword)

def scrape_website(url, keyword):
    try:
        # ページごとの情報を格納するリスト
        results = []

        # 初回のリクエスト
        response = requests.get(url)
        response.raise_for_status()

        # ページネーションのリンクを探し、ページをスクレイピング
        while True:
            soup = BeautifulSoup(response.text, 'html.parser')

            title = soup.title.text
            result = f'Title: {title}\n\n'

            page_url = response.url
            result += f'URL: {page_url}\n\n'

            page_text = ' '.join([p.get_text() for p in soup.find_all(['p', 'div'])])
            result += f'キーワード "{keyword}" を含むページテキスト:\n\n'

            keyword_text = [line.strip() for line in page_text.splitlines() if keyword in line]
            for line in keyword_text:
                result += f'{line}\n'

            # キーワードで検索して取得したサイトのすべてのリンクについてURLも表示
            keyword_links = [(a['href'], a.get_text()) for a in soup.find_all('a', href=True) if keyword in a.get_text()]
            if keyword_links:
                result += '\nキーワードに関連するリンク:\n'
                for keyword_link, keyword_title in keyword_links:
                    full_keyword_link = urljoin(url, keyword_link)
                    result += f'[{keyword_title}]({full_keyword_link}) - {full_keyword_link}\n'

            # 結果をリストに追加
            results.append(result)

            # 次のページに移動
            next_page_link = soup.find('a', text='next') or soup.find('a', text='次へ') or soup.find('a', text='次のページ')
            if not next_page_link:
                break

            next_page_url = urljoin(url, next_page_link['href'])
            response = requests.get(next_page_url)
            response.raise_for_status()

        # 最終的な結果を表示
        st.text_area("検索結果:", value='\n\n'.join(results), height=400)

    except requests.exceptions.RequestException as e:
        error_message = f"ページの取得に失敗しました。エラー: {e}"
        st.text_area("検索結果:", value=error_message, height=400)

if __name__ == "__main__":
    main()





















