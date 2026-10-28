import requests
from bs4 import BeautifulSoup

#ずっと繰り返すようにする
While True :

    # 入力欄（前後の空白を除去）
    user_input = input("\n 取得したいページのURLを入力してください: ").strip()

    # https:// や http:// で始まっていない場合は自動で付与する
    if not user_input.startswith(("http://", "https://")):
        url = "https://" + user_input
    else:
        url = user_input

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        response.encoding = response.apparent_encoding

        soup = BeautifulSoup(response.text, "html.parser")

        # 不要なタグを削除
        for element in soup(["script", "style", "header", "footer", "nav", "aside"]):
            element.decompose()

        # 記事本文が含まれる範囲を優先的に探す（見つからない場合は全体）
        main_content = soup.find("article") or soup.find("main") or soup

        clean_text = main_content.get_text(separator="\n", strip=True)
        print("\n--- 取得結果 --- \n ")
        print(clean_text)
    
    except requests.exceptions.RequestException as e:
        print(f"エラーが発生しました: {e}")
