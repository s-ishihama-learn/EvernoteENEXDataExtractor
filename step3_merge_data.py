"""
ベースデータと追加データをマージし、整形して新しいCSVファイルを作成するモジュール。
"""
import os
import sys  # pylint: disable=unused-import
import csv
import pandas as pd

def main():
    """
    メイン処理を実行する。
    ベースデータと追加データを読み込み、マージ、ソート、連番採番を行い、
    結果を新しいCSVファイルとして保存する。
    """
    # スクリプトのあるディレクトリを基準にパスを設定
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # ファイルパス定義
    # step1で作成されたベースデータ
    base_csv_path = os.path.join(base_dir, 'data', 'data_base.csv')
    # step2で作成された追加データ
    # ※プロンプトでは「data_new.csvを読み込む」とありましたが、文脈（step2の出力）から
    #   data_add.csv が正しい入力ファイルであると判断して使用します。
    add_csv_path = os.path.join(base_dir, 'data', 'data_add.csv')
    # 出力ファイル
    output_csv_path = os.path.join(base_dir, 'data', 'data_new.csv')

    print(f"Base data: {base_csv_path}")
    print(f"Add data: {add_csv_path}")
    print(f"Output data: {output_csv_path}")

    # ファイルの存在確認
    if not os.path.exists(base_csv_path):
        print(f"エラー: ベースデータが見つかりません: {base_csv_path}")
        return
    
    if not os.path.exists(add_csv_path):
        print(f"エラー: 追加データが見つかりません: {add_csv_path}")
        return

    try:
        # 1. data/data_base.csvをpandasデータとして読み込む
        print("ベースデータを読み込み中...")
        df_base = pd.read_csv(base_csv_path, encoding='utf-8')
        
        # 2. data/data_add.csvをpandasデータとして読み込む
        # step2の出力はヘッダーがないため、df_baseのカラム名を使用します
        print("追加データを読み込み中...")
        if os.path.getsize(add_csv_path) > 0:
            df_add = pd.read_csv(add_csv_path, encoding='utf-8', header=None, names=df_base.columns)
        else:
            print("追加データが空です。")
            df_add = pd.DataFrame(columns=df_base.columns)

        # 3. 読み込んだdata/data_base.csvのpandasデータにdata/data_add.csvのpandasデータを追加してマージ
        print("データをマージ中...")
        df_merged = pd.concat([df_base, df_add], ignore_index=True)

        # 4. マージしたデータを「取得日」の新しい順にソート
        print("データをソート中...")
        # 日付型に変換してソート（エラー値はNaTにして末尾へ）
        df_merged['temp_date'] = pd.to_datetime(df_merged['取得日'], errors='coerce')
        df_merged = df_merged.sort_values(by='temp_date', ascending=False)
        df_merged = df_merged.drop(columns=['temp_date'])

        # 5. ソートしたデータの「No.」を１から連番で採番する
        print("No.を採番中...")
        df_merged['No.'] = range(1, len(df_merged) + 1)

        # 6. 処理した結果をdata/data_new.csvというファイル名で、CSVファイルとして出力する
        print(f"保存中: {output_csv_path}")
        df_merged.to_csv(output_csv_path, index=False, encoding='utf-8', quoting=csv.QUOTE_NONNUMERIC)
        print("完了しました。")

    except Exception as e:  # pylint: disable=broad-except
        print(f"エラーが発生しました: {e}")
        import traceback  # pylint: disable=import-outside-toplevel
        traceback.print_exc()

if __name__ == "__main__":
    main()