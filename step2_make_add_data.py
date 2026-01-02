"""
Evernoteのエクスポートファイル（.enex）からノート情報を抽出し、
ベイジアンフィルタでカテゴリを予測してCSVファイルに追加データとして保存するモジュール。
"""
import xml.etree.ElementTree as ET
import glob
import os
import csv
from datetime import datetime
from bayesian_filter import BayesianFilter  # @UnresolvedImport # pylint: disable=import-error

bf = BayesianFilter()  # pylint: disable=invalid-name
bf.load("type_predict")

def predict(title):
    """
    与えられたタイトルからカテゴリを予測する。

    Args:
        title (str): 予測対象のタイトル。

    Returns:
        str: 予測されたカテゴリ。
    """
    pre, score_list, word_count = bf.predict(title)
    print(pre, score_list, word_count)
    return pre

def extract_from_enex(file_path, output_path=None):
    """
    Evernoteのenexファイルを解析し、タイトルとURL(source-url)を抽出してCSVに出力します。

    Args:
        file_path (str): 解析対象の.enexファイルのパス。
        output_path (str, optional): 出力先のCSVファイルのパス。
                                     指定しない場合はファイルへの書き込みは行われません。
                                     Defaults to None.
    """
    print(f"--- Processing: {file_path} ---")
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        count = 0
        for note in root.findall('note'):
            title = note.find('title').text if note.find('title') is not None else "No Title"
            
            created_text = note.find('created').text if note.find('created') is not None else None
            created = "Unknown Date"
            if created_text:
                try:
                    created = datetime.strptime(created_text, '%Y%m%dT%H%M%SZ').strftime('%Y-%m-%d')
                except ValueError:
                    created = created_text
            
            # WebクリップのURLは note-attributes -> source-url に格納されています
            attributes = note.find('note-attributes')
            source_url = None
            if attributes is not None:
                source_url_node = attributes.find('source-url')
                if source_url_node is not None:
                    source_url = source_url_node.text

            if source_url:
                count += 1
                if output_path:
                    with open(output_path, 'a', encoding='utf-8', newline='') as f:
                        ptype = predict(title)
                        writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
                        writer.writerow([count, source_url, title, created, ptype])
        
        print(f"Found {count} notes with URLs.")

    except Exception as e:  # pylint: disable=broad-except
        print(f"Error parsing {file_path}: {e}")

if __name__ == "__main__":
    # スクリプトのあるディレクトリを取得
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # "Evernoteエクスポート" ディレクトリ内の .enex ファイルを探して処理します
    target_dir = os.path.join(base_dir, "Evernoteエクスポート")
    enex_files = glob.glob(os.path.join(target_dir, "*.enex"))

    # 出力先のファイルパスを設定 (data/data_add.csv)
    output_path = os.path.join(base_dir, "data", "data_add.csv")
    # ディレクトリが存在しない場合は作成
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    # ファイルを初期化（上書きモードで空にする）
    with open(output_path, 'w', encoding='utf-8') as f:
        pass
    
    if enex_files:
        for enex_file in enex_files:
            extract_from_enex(enex_file, output_path)
    else:
        print(f"No .enex files found in: {target_dir}")