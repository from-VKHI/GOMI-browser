import requests
from bs4 import BeautifulSoup

# ずっと繰り返すようにする
while True:
    # 入力欄（前後の空白を除去）
    user_input = input("\n ---------------------------------------------- \n 取得したいページのURLを入力してください (終了は q): ").strip()

    # 何も入力されずにEnterが押された場合は再入力
    if not user_input:
        continue

    # 「q」または「exit」でプログラムを終了できるようにする
    if user_input.lower() in ["q", "exit", "quit"]:
        print("\n------------------プログラムを終了します。------------------\n")
        break

    # 大文字で入力された場合（HTTPS:// など）も考慮して小文字でチェック
    if not user_input.lower().startswith(("http://", "https://")):
        url = "https://" + user_input
    else:
        url = user_input

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        try:
            # まずは設定されたURLでアクセス
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            # https:// で失敗し、かつ元々 http:// や https:// が入力されていなかった場合は http:// を試す
            if not user_input.lower().startswith(("http://", "https://")):
                url = "http://" + user_input
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
            else:
                raise e

        response.encoding = response.apparent_encoding

        soup = BeautifulSoup(response.text, "html.parser")

        # 不要なタグを削除
        for element in soup(["script", "style", "header", "footer", "nav", "aside"]):
            element.decompose()

        # 記事本文が含まれる範囲を優先的に探す（見つからない場合は全体）
        main_content = soup.find("article") or soup.find("main") or soup

        clean_text = main_content.get_text(separator="\n", strip=True)
        print("\n -------------------- 取得結果 -------------------- \n")
        print(clean_text)

    except requests.exceptions.RequestException as e:
        print(f"\n ---------------------------------------------- \n エラーが発生しました: \n {e} \n ---------------------------------------------- \n")
