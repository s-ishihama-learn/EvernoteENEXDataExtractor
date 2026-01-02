"""
CSVデータを読み込み、JavaScriptファイル（data.js）として出力するモジュール。
HTMLのテーブル行として整形されたデータを含む。
"""
import os
import pandas as pd

def truncate_title(title, max_bytes=150):
    """
    タイトルをバイト数で切り詰め、末尾に '...' を付与する。
    漢字が途中で切れないように文字単位で処理する。

    Args:
        title (str): 切り詰めるタイトル文字列。
        max_bytes (int): 最大バイト数。デフォルトは150。

    Returns:
        str: 切り詰められたタイトル。
    """
    if not isinstance(title, str):
        return title

    if len(title.encode('utf-8')) <= max_bytes:
        return title

    result = ""
    current_byte_len = 0
    for char in title:
        char_byte_len = len(char.encode('utf-8'))
        # '...' の3バイト分を考慮して、追加後のバイト数がmax_bytesを超えないようにする
        if current_byte_len + char_byte_len + 3 > max_bytes:
            break
        result += char
        current_byte_len += char_byte_len
    
    return result + " ..."

def main():
    """
    メイン処理を実行する。
    CSVファイルを読み込み、HTMLタグを含むJavaScript変数として出力する。
    """
    # スクリプトのあるディレクトリを基準にパスを設定
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(base_dir, 'data', 'data_new.csv')
    output_path = os.path.join(base_dir, 'EvernoteToHtml', 'data.js')

    df = pd.read_csv(input_path)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('const dataList = `\n')

        for _, row in df.iterrows():
            truncated_title = truncate_title(row["タイトル"])
            # pylint: disable=line-too-long
            line = f'<tr><td class="text-center">{row["No."]}</td><td><a href="{row["URL"]}" target="blank">{truncated_title}</a><td class="text-center">{row["取得日"]}</td><td>{row["新分類"]}</td></tr>'
            f.write(line + '\n')

        f.write('`;')

if __name__ == '__main__':
    main()