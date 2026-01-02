"""
データファイルとExcelファイルを読み込み、マージしてベースデータを作成するモジュール。
"""
import os
import re  # pylint: disable=unused-import
import sys
import csv

# pandasとopenpyxlがインストールされているか確認
try:
    import pandas as pd
except ImportError:
    print("エラー: pandas がインストールされていません。")
    print("以下のコマンドを実行してインストールしてください:")
    print("pip install pandas openpyxl")
    sys.exit(1)

def main():
    """
    メイン処理を実行する。
    データCSVとExcelファイルを読み込み、マージして新しいCSVファイルを出力する。
    """
    # スクリプトのあるディレクトリを基準にパスを設定
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, 'data', 'data.csv')
    excel_path = os.path.join(base_dir, 'data', '未分類.xlsx')

    print(f"data.jsパス: {data_path}")
    print(f"Excelファイルパス: {excel_path}")

    # data.jsファイルの存在確認
    if not os.path.exists(data_path):
        print(f"エラー: data.jsファイルが見つかりません: {data_path}")
        return

    # Excelファイルの存在確認
    if not os.path.exists(excel_path):
        print(f"エラー: Excelファイルが見つかりません: {excel_path}")
        return

    # Excelデータの読み込み
    try:
        # A列(No.)とF列(新分類)を読み込む (0-indexedで 0と5)
        df_data = pd.read_csv(data_path, encoding='utf-8', names=["No.", "URL", "タイトル", "取得日", "分類"])
        df_excel = pd.read_excel(excel_path, usecols=[0, 5])
        df = pd.merge(df_data, df_excel, left_on=df_data.columns[0], right_on=df_excel.columns[0], how='left')
        df['新分類'] = df['新分類'].fillna(df['分類'])
        df = df.drop('分類', axis=1)
        df['No.'] = range(1, len(df) + 1)

        output_path = os.path.join(base_dir, 'data', 'data_base.csv')
        df.to_csv(output_path, index=False, encoding='utf-8', quoting=csv.QUOTE_NONNUMERIC)
        print(f"保存しました: {output_path}")

    except Exception as e:  # pylint: disable=broad-except
        print(f"Excel読み込み中にエラーが発生しました: {e}")
        return

if __name__ == "__main__":
    main()