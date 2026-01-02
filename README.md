# Evernote ENEX Data Extractor

このスクリプトは、Evernoteからエクスポートされた `.enex` ファイルを解析し、Webクリップの情報を抽出してCSVファイルに保存するツールです。また、ベイジアンフィルタを使用してタイトルに基づきカテゴリ予測を行います。

## 機能

1. 分類「未分類」を含む`data/data.csv`と`data/未分類.xlsx`を結合して、「未分類」に分類を設定します。`data/data_base.csv`を出力します。
2. `data/data_base.csv`を使用して、タイトルから分類を予測するためのモデルを作成します。
   - 分類
      * 生成AI
      * 機械学習
      * ITシステム
      * プログラミング
      * 経営・コンサル
      * チーム・組織
      * 社会課題
      * 自己啓発
      * 起業・副業
      * 雑学

3. `Evernoteエクスポート` ディレクトリ内の `.enex` ファイルを検索します。
4. 各ノートから以下の情報を抽出します:
   - タイトル
   - 作成日
   - ソースURL (Webクリップの場合)
5. `bayesian_filter` モジュールを使用して、タイトルからカテゴリを予測します。
6. 抽出したデータを `data/data_add.csv` に出力します。
7. `data/data_base.csv`と `data/data_add.csv` を結合して`data/data_new.csv` に出力します。
8. `data/data_new.csv` からhtml表示用の`EvernoteToHtml/data.js`を作成します。


## 必要要件

- Python 3.x
- `bayesian_filter.py` (同ディレクトリに配置されている必要があります)
- `type_predict` (学習済みのモデルファイル)

## ディレクトリ構成

スクリプトを実行する前に、以下のディレクトリ構成を確認してください。

```text
.
├── step1_set_type_base.py  # 未分類の結合スクリプト
├── step2_make_add_data.py  # Evernoteエクスポートファイル読込スクリプト
├── step3_merge_data.py     # ファイル結合スクリプト
├── step4_make_js.py        # JavaScript作成スクリプト
├── bayesian_filter.py      # ベイジアンフィルタモジュール
├── type_predict.py         # ベイジアンフィルタによる学習モデル
├── type_predict            # 学習済みモデルデータ
├── Evernoteエクスポート/    # .enexファイルを格納するディレクトリ
│   └── *.enex
├── EvernoteToHtml/
│   └── data.js             # html表示用JavaScript（最終出力ファイル）
└── data/                   # 出力先ディレクトリ (自動作成されます)
    ├── data.csv            # 「未分類」を含むオリジナルデータ
    ├── 未分類.xlsx          # 「未分類」に対応する分類データ
    ├── data_base.csv       # data.csvに「未分類」を置き換えたデータ
    ├── data_add.csv        # Evernoteエクスポートファイルから抽出したデータ
    └── data_new.csv        # オリジナルデータと追加データの結合データ
 ```

## 使い方

1. `Evernoteエクスポート` ディレクトリを作成し、解析したい `.enex` ファイルを配置します。
   - Evernoteを開く
   - エクスポートするノートブックを右クリックして、「ノートブックをエクスポート」
   - `.enex` ファイルを`Evernoteエクスポート` ディレクトリに配置します。
2. スクリプトを実行します。
   - step2_make_add_data.pyを実行します。
   - step3_merge_data.pyを実行します。
   - step4_make_js.pyを実行します。

```bash
python step2_make_add_data.py
python step3_merge_data.py
python step4_make_js.py
```

3. 処理が完了すると、`EvernoteToHtml/data.js` に結果が保存されます。