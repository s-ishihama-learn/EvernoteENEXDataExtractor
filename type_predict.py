"""
ベイジアンフィルタを用いたカテゴリ予測を行うモジュール。
"""
import pandas as pd
from bayesian_filter import BayesianFilter  # @UnresolvedImport # noqa # pylint: disable=import-error


def make_type_predict_data():
    """
    学習データを作成し、モデルを保存する。
    """
    bf = BayesianFilter()
    df = pd.read_csv("data/data_base.csv")
    for index, row in df.iterrows():
        if index % 1000 == 0:
            print(index)
        bf.fit(row["タイトル"], row["新分類"])
    bf.save("type_predict")


def predict(title):
    """
    タイトルからカテゴリを予測する。

    Args:
        title (str): 予測したいタイトル

    Returns:
        str: 予測結果のカテゴリ
    """
    bf = BayesianFilter()
    bf.load("type_predict")

    # 予測
    pre, score_list, word_count = bf.predict(title)
    print(pre, score_list, word_count)
    return pre


if __name__ == "__main__":
    make_type_predict_data()
    predict("「急いで作って！」と言われたとき、私がまずやること→Miroだけでスクラム")
