"""
追加データに新たな.enexのデータをマージし、既存のCSVファイルに追加するモジュール。
"""
import glob
import os
import sys  # pylint: disable=unused-import
import step2_make_add_data as step2


if __name__ == "__main__":
    # スクリプトのあるディレクトリを取得
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # "Evernoteエクスポート" ディレクトリ内の .enex ファイルを探して処理します
    target_dir = os.path.join(base_dir, "Evernoteエクスポート")
    enex_files = glob.glob(os.path.join(target_dir, "*.enex"))

    # 出力先のファイルパスを設定 (data/data_add.csv)
    output_path = os.path.join(base_dir, "data", "data_add.csv")
    
    if enex_files:
        for enex_file in enex_files:
            step2.extract_from_enex(enex_file, output_path)
    else:
        print(f"No .enex files found in: {target_dir}")