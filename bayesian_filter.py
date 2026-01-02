"""ベイジアンフィルタを実装したモジュール。"""

import sys
import math
import json
from collections import OrderedDict
# 形態素解析用
from janome.analyzer import Analyzer
from janome.charfilter import UnicodeNormalizeCharFilter, RegexReplaceCharFilter
from janome.tokenfilter import POSKeepFilter
from janome.tokenizer import Tokenizer


class BayesianFilter:
    """ベイジアンフィルタクラス。"""

    def __init__(self):
        self.words = set()  # 出現した単語を全て記録
        self.word_dict = {}  # カテゴリごとの単語出現回数を記録
        self.category_dict = {}  # カテゴリの出現回数を記録

        # 対象とする品詞体系
        token_filters = [POSKeepFilter(['名詞', '形容詞', '連体詞', '副詞', '動詞'])]

        # 除外文字
        char_reg_filter = [(r"[,\.\(\)\{\}\[\]\!]", " ")]
        char_filters = [UnicodeNormalizeCharFilter()]
        for reg in char_reg_filter:
            char_filters.append(RegexReplaceCharFilter(*reg))

        # 形態素解析用
        tokenizer = Tokenizer()
        self.analyzer = Analyzer(char_filters=char_filters, tokenizer=tokenizer, token_filters=token_filters)

    # 単語を数える処理
    def inc_word(self, word, category):
        """
        カテゴリごとに単語の出現回数を数える。

        Args:
            word (str): 単語
            category (str): カテゴリ
        """
        # 単語をカテゴリに追加
        if not category in self.word_dict:
            self.word_dict[category] = {}
        if not word in self.word_dict[category]:
            self.word_dict[category][word] = 0
        self.word_dict[category][word] += 1
        self.words.add(word)

    # カテゴリを数える処理
    def inc_category(self, category):
        """
        カテゴリの出現回数を数える。

        Args:
            category (str): カテゴリ
        """
        # カテゴリを加算する
        if not category in self.category_dict:
            self.category_dict[category] = 0
        self.category_dict[category] += 1

    # テキストを学習す
    def fit(self, text, category):
        """
        テキストを学習する。

        Args:
            text (str): 学習するテキスト
            category (str): テキストのカテゴリ
        """
        word_list = [token.surface for token in self.analyzer.analyze(text)]
        for word in word_list:
            self.inc_word(word, category)
        self.inc_category(category)

    # カテゴリ/総カテゴリを計算
    def category_prob(self, category):
        """
        カテゴリの出現確率を計算する。

        Args:
            category (str): カテゴリ

        Returns:
            float: カテゴリの出現確率
        """
        sum_categories = sum(self.category_dict.values())
        category_v = self.category_dict[category]
        return category_v / sum_categories

    # カテゴリ内の単語の出現率を計算
    def word_prob(self, word, category):
        """
        カテゴリ内での単語の出現確率を計算する（ラプラススムージング適用）。

        Args:
            word (str): 単語
            category (str): カテゴリ

        Returns:
            float: カテゴリ内での単語の出現確率
        """
        # pylint: disable=invalid-name
        n = self.get_word_count(word, category) + 1  # 分子 (numerator)
        d = sum(self.word_dict[category].values()) + len(self.words)  # 分母 (denominator)
        return n / d

    # カテゴリ内の単語出現数を得る
    def get_word_count(self, word, category):
        """
        カテゴリ内での単語の出現回数を取得する。

        Args:
            word (str): 単語
            category (str): カテゴリ

        Returns:
            int: 単語の出現回数
        """
        if word in self.word_dict[category]:
            return self.word_dict[category][word]
        return 0

    # カテゴリにおける単語リストのスコアを計算する
    def score(self, words, category):
        """
        単語リストが与えられたカテゴリに属するスコア（対数確率）を計算する。

        Args:
            words (list): 単語のリスト
            category (str): カテゴリ
        """
        score = math.log(self.category_prob(category))
        for word in words:
            score += math.log(self.word_prob(word, category))
        return score

    # テキストのカテゴリ分けを行う
    def predict(self, text):
        """
        テキストのカテゴリを予測する。

        Args:
            text (str): 予測したいテキスト

        Returns:
            tuple: (最適なカテゴリ, カテゴリごとのスコアリスト, 単語数)
        """
        best_category = None
        max_score = -sys.maxsize
        words = [token.surface for token in self.analyzer.analyze(text)]
        score_list = []
        for category in self.category_dict.keys():
            score = self.score(words, category)
            score_list.append((category, score))
            if score > max_score:
                max_score = score
                best_category = category
        return best_category, score_list, len(words)

    # 単語の出現率をファイルに保存
    def save(self, file_path):
        """
        学習データをJSONファイルに保存する。

        Args:
            file_path (str): 保存するファイルのパス（拡張子なし）
        """
        with open(file_path + '_word.json', 'w', encoding='utf-8') as f:
            json.dump(self.word_dict, f, ensure_ascii=False, indent=4)

        with open(file_path + '_category.json', 'w', encoding='utf-8') as f:
            json.dump(self.category_dict, f, ensure_ascii=False, indent=4)

    # 単語の出現率をファイルから読み込み
    def load(self, file_path):
        """
        学習データをJSONファイルから読み込む。

        Args:
            file_path (str): 読み込むファイルのパス（拡張子なし）
        """
        with open(file_path + '_word.json', 'r', encoding='utf-8') as f:
            self.word_dict = json.load(f)

        with open(file_path + '_category.json', 'r', encoding='utf-8') as f:
            self.category_dict = json.load(f)

        for category in self.category_dict.keys():
            for word in self.word_dict[category].keys():
                self.words.add(word)

    # 上位スコアのカテゴリを抽出
    # pylint: disable=too-many-locals
    def top_score(self, score_list, size=3, log_value=True, word_count=0):
        """
        スコアリストから上位のカテゴリを抽出する。

        Args:
            score_list (list): (カテゴリ, スコア) のタプルのリスト
            size (int, optional): 抽出する上位カテゴリの数. Defaults to 3.
            log_value (bool, optional): Trueの場合、対数スコアをそのまま返す.
                                        Falseの場合、正規化された確率を返す.
                                        Defaults to True.
            word_count (int, optional): テキストの単語数. log_valueがFalseの場合に必要.
                                        Defaults to 0.

        Returns:
            OrderedDict: 上位カテゴリとそのスコア（または確率）
        """
        # 確率の高い順に並び替え
        score_dic = {}
        for score in score_list:
            score_dic[score[0]] = score[1]
        score_sort = sorted(score_dic.items(), key=lambda x: -x[1])

        # 上位スコアの抽出
        top_dic = OrderedDict()
        if log_value:
            # logの算出値をそのまま返す
            count = 0
            for score in score_sort:
                top_dic[score[0]] = score[1]
                count += 1
                if count >= size:
                    break

        else:
            # size数で、合計が1.0になるように正規化して返す
            word_size = float(len(self.words))
            word_rate = 1.0 / float(word_count + 1.0)

            total_score = 0.0
            count = 0
            for score in score_sort:
                value = math.pow(math.exp(score[1]) * word_size, word_rate)
                top_dic[score[0]] = value
                total_score += value
                count += 1
                if count >= size:
                    break
            for key in top_dic:
                top_dic[key] /= total_score

        return top_dic
