# タイプアノテーションで func(self) -> 自身のクラス名  とするために必要
from __future__ import annotations
import random
import copy


class Card:
    # Card("♥2") のような指定でCardクラスを生成できる
    def __init__(self, suit_and_rank) -> None:
        self.suit = suit_and_rank[0]  # suitは 1 文字
        self.rank = suit_and_rank[1:]  # rankは 1 or 2 文字

    # Cardクラスに対して str() を使用したときの文字列表現を提供
    def __str__(self) -> str:
        return f"{self.suit}{self.rank}"

    # Cardクラスの文字列表現を提供(テストエラー時の表示を見やすくする)
    def __repr__(self) -> str:
        return f'Card("{self.suit}{self.rank}")'

    # Cardクラスに対して == で判定するには __eq__ が必要
    def __eq__(self, value: object) -> bool:
        # 比較対象が、Cardクラス のインスタンスなら、以下の式で比較
        if isinstance(value, Card):
            return self.suit == value.suit and self.rank == value.rank
        # それ以外なら、イコールではない
        return False

    # Cardクラスに対して set を使うには __hash__ が必要
    def __hash__(self) -> int:
        return hash((self.suit, self.rank))


class Cards:
    # トランプに含まれる マーク と 番号 の定義
    _SUITS = ("♥", "♦", "♣", "♠")
    _RANKS = ("2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A")

    # Cards() もしくは Cards("♥2 ♥4") のような指定でクラスを生成できる
    def __init__(self, cards_str: str | None = None) -> None:
        if cards_str is None:
            self._items = []
        else:
            self._items = [Card(card_str) for card_str in cards_str.split(" ")]

    @classmethod
    def create_deck(cls) -> Cards:
        """トランプのデッキを生成する"""
        cards = cls()
        for suit in cls._SUITS:
            for rank in cls._RANKS:
                cards.add(Card(suit + rank))
        return cards

    # Cardsクラスに対して == で判定するには __eq__ が必要
    def __eq__(self, value: object) -> bool:
        if isinstance(value, Cards):
            return self._items == value._items
        return False

    def __str__(self):
        return " ".join([str(item) for item in self._items])

    def __len__(self) -> int:
        return len(self._items)

    def items(self) -> list[Card]:
        return self._items[:]

    def suits(self) -> set[str]:
        return {card.suit for card in self._items}

    def ranks(self) -> set[str]:
        return {card.rank for card in self._items}

    def rank_indexes(self) -> set[int]:
        """各カードの rank の集合を、下記のようにインデックスに変換して返す

        変換規則 "2"->0, "3"->1, ... "10"->8, "J"->9, "Q"->10, "K"->11, "A"->12
        """
        return {self._RANKS.index(r) for r in self.ranks()}

    def rank_counts(self) -> list[int]:
        """各 rank のカードが、それぞれ何枚含まれるかをリストにして返す

        リストの並びは [2, 3, 4 ... 9, 10, J, K, Q, A] の順になる
        """
        ranks = [card.rank for card in self._items]
        return [ranks.count(r) for r in self._RANKS]

    def remove(self, indexes: list[int]):
        # 要素の削除による配列のインデックス変化の影響を受けないように
        # 削除するインデックスを降順に並べ替えてから、要素を削除する
        for index in sorted(indexes, reverse=True):
            del self._items[index]

    def add(self, card: Card) -> None:
        self._items.append(card)

    def draw(self) -> Card:
        # リストの先頭から要素を取り出す
        # 最後から取り出すより、見た目の動作が理解しやすいので
        return self._items.pop(0)

    def shuffle(self) -> None:
        random.shuffle(self._items)


class Deck:
    def __init__(self, cards_str: str | None = None) -> None:
        """
        - Deck() で、通常の山札を生成
        - Deck("♥2 ♥4") で、指定のカードで山札を生成(主に、テストで使用)
        """
        if cards_str is None:
            self._cards = Cards.create_deck()
        else:
            self._cards = Cards(cards_str)

    def __len__(self) -> int:
        return len(self._cards)

    def cards(self) -> list[Card]:
        return self._cards.items()

    def draw(self) -> Card:
        return self._cards.draw()

    def shuffled(self) -> Deck:
        # 元のクラスは変更せず、新しいインスタンスを返すようにする
        # 通常、メソッドチェーンは非破壊で実装するようなので
        cloned_cards = copy.deepcopy(self._cards)
        cloned_cards.shuffle()
        new_deck = Deck()
        new_deck._cards = cloned_cards
        return new_deck


class Hand:
    # Hand() もしくは Hand("♥2 ♥4") のような指定でクラスを生成できる
    def __init__(self, cards_str: str | None = None) -> None:
        self._cards = Cards(cards_str)

    # Handクラスに対して == で判定するには __eq__ が必要
    def __eq__(self, value: object) -> bool:
        if isinstance(value, Hand):
            return self._cards == value._cards
        return False

    def __str__(self) -> str:
        return str(self._cards)

    def __len__(self) -> int:
        return len(self._cards)

    def cards(self) -> list[Card]:
        return self._cards.items()

    def add(self, card: Card) -> None:
        self._cards.add(card)

    def remove(self, indexes: list[int]) -> None:
        self._cards.remove(indexes)

    def has_enough_cards(self) -> bool:
        """手札に5枚のカードがある"""
        return len(self._cards) == 5

    def judge(self) -> str:
        """手札の役を判定する"""
        return Judge(self._cards).execute()


class Judge:
    def __init__(self, cards: Cards) -> None:
        self._cards = cards

    def execute(self) -> str:
        if self._is_royal() and self._is_flush():
            return "Royal Flush"
        if self._is_straight() and self._is_flush():
            return "Straight Flush"
        elif self._four_card_exist():
            return "Four of a Kind"
        elif self._three_card_exist() and (self._num_of_pair_card() == 1):
            return "Full House"
        elif self._is_flush():
            return "Flush"
        elif self._is_straight():
            return "Straight"
        elif self._three_card_exist():
            return "Three of a Kind"
        elif self._num_of_pair_card() == 2:
            return "Two Pair"
        elif self._num_of_pair_card() == 1:
            return "One Pair"
        return "High Card"

    def _is_royal(self) -> bool:
        #  rank が 10,J,Q,K,A なら、ロイヤル(フラッシュ)
        return self._cards.ranks() == {"10", "J", "Q", "K", "A"}

    def _is_flush(self) -> bool:
        # suit が 1 種類になら、フラッシュ
        return len(self._cards.suits()) == 1

    def _is_straight(self) -> bool:
        # rank が5種類でなかったら、ストレートではない(rank に重複があるので)
        if len(self._cards.ranks()) != 5:
            return False
        # 各 rank をインデックスに変換し、最小・最大を計算
        # その差が 4 なら、rank が5枚連続しているので、ストレートである
        max_index = max(self._cards.rank_indexes())
        min_index = min(self._cards.rank_indexes())
        if (max_index - min_index) == 4:
            return True
        # 上記で判定できない特殊ケースとして A,2,3,4,5 もストレート
        if self._cards.ranks() == {"A", "2", "3", "4", "5"}:
            return True
        return False

    def _four_card_exist(self) -> bool:
        # いずれかの rank のカードが、手札に 4枚 含まれている
        return 4 in self._cards.rank_counts()

    def _three_card_exist(self) -> bool:
        # いずれかの rank のカードが、手札に 3枚 含まれている
        return 3 in self._cards.rank_counts()

    def _num_of_pair_card(self) -> int:
        """ペアの数"""
        # ペアが成立している(手札に 2枚 含まれている) rank の数を返す
        return self._cards.rank_counts().count(2)


class Dealer:
    def deal_cards(self, deck: Deck, hand: Hand) -> None:
        """カードを配る"""
        while not hand.has_enough_cards():
            hand.add(deck.draw())


class Poker:
    def __init__(self, dealer: Dealer, shuffled_deck: Deck, hand: Hand) -> None:
        self._dealer = dealer
        self._deck = shuffled_deck
        self._hand = hand

    def play(self) -> None:
        # カードを配る
        self._dealer.deal_cards(self._deck, self._hand)
        print("あなたの手札")
        print(self._hand)
        # 手札から指定のカードを捨てる
        card_indexes = self.select_exchange_cards()
        self._hand.remove(card_indexes)
        # カードを配る
        self._dealer.deal_cards(self._deck, self._hand)
        print("交換結果")
        print(self._hand)
        # 手札の役を表示する
        print(f"結果は {self._hand.judge()} です")

    def select_exchange_cards(self) -> list[int]:
        indexes_input = input("交換するカードの番号(0-4)をスペース区切りで入力: ")
        return [int(index) for index in indexes_input.split()]


if __name__ == "__main__":
    poker = Poker(Dealer(), Deck().shuffled(), Hand())
    poker.play()
