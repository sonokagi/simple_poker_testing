from poker import Card, Cards, Deck, Hand, Dealer, Poker
import unittest
from io import StringIO
from unittest.mock import patch


class TestCard(unittest.TestCase):
    def test_creation(self):
        Card("♥A")

    def test_suit(self):
        self.assertEqual(Card("♥A").suit, "♠")

    def test_rank(self):
        self.assertEqual(Card("♥A").rank, "A")

    def test_can_use_str(self):
        self.assertEqual(str(Card("♥A")), "♥A")
        self.assertEqual(str(Card("♠2")), "♠2")

    def test_can_use_equal(self):
        self.assertEqual(Card("♥A"), Card("♥A"))
        self.assertNotEqual(Card("♥A"), Card("♠A"))
        self.assertNotEqual(Card("♥A"), Card("♥2"))

    def test_can_use_set(self):
        # 集合にすると、同じカードは除去され、要素の並びは影響しなくなる
        self.assertEqual(
            {Card("♥A"), Card("♥A"), Card("♠A"), Card("♥2")},
            {Card("♥2"), Card("♠A"), Card("♥A")},
        )


class TestCards(unittest.TestCase):
    suits = ("♠", "♦", "♣", "♥")
    ranks = ("2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A")

    def test_creation(self):
        Cards()
        Cards("♥2 ♥4 ♥6 ♥8 ♠10")
        Cards.create_deck()

    def test_items(self):
        self.assertEqual(Cards().items(), [])

        self.assertEqual(
            Cards("♥2 ♥4 ♥6 ♥8 ♠10").items(),
            [Card("♥2"), Card("♥4"), Card("♥6"), Card("♥8"), Card("♠10")],
        )

        # 各カードのリストへの格納順序は問わない。このため、集合に変換して比較する
        self.assertEqual(
            set(Cards.create_deck().items()),
            set([Card(s + r) for s in self.suits for r in self.ranks]),
        )

    def test_can_use_equal(self):
        self.assertEqual(Cards("♥1 ♥2"), Cards("♥1 ♥2"))
        self.assertNotEqual(Cards("♥1 ♥2"), Cards("♥2 ♥1"))
        self.assertNotEqual(Cards("♥1 ♥2"), Cards("♥1 ♥2 ♥3"))

    def test_can_use_str(self):
        self.assertEqual(str(Cards()), "")
        self.assertEqual(str(Cards("♥2 ♥4 ♥6 ♥8 ♠10")), "♥2 ♥4 ♥6 ♥8 ♠10")

    def test_can_use_len(self):
        self.assertEqual(len(Cards()), 0)
        self.assertEqual(len(Cards("♥2 ♥4 ♥6 ♥8 ♠10")), 5)

    def test_suits(self):
        test_pattern = [
            # カードの組み合わせ, 期待値(各 suit の集合)
            ("♥2", {"♥"}),
            ("♥2 ♥3", {"♥"}),
            ("♥2 ♦2 ♣2 ♠2", {"♥", "♦", "♣", "♠"}),
        ]
        for cards_str, expect in test_pattern:
            self.assertEqual(Cards(cards_str).suits(), expect)

    def test_ranks(self):
        test_pattern = [
            # カードの組み合わせ, 期待値(各 rank の集合)
            ("♥2", {"2"}),
            ("♥2 ♦2", {"2"}),
            ("♥2 ♥3 ♥4 ♥5 ♥6", {"2", "3", "4", "5", "6"}),
        ]
        for cards_str, expect in test_pattern:
            self.assertEqual(Cards(cards_str).ranks(), expect)

    def test_rank_indexes(self):
        test_pattern = [
            # カードの組み合わせ, 期待値(各 rank のインデックス集合)
            ("♥2", {0}),
            ("♥2 ♦2", {0}),
            ("♥2 ♥3 ♥4 ♥5 ♥6", {0, 1, 2, 3, 4}),
            ("♥6 ♥7 ♥8 ♥9 ♥10", {4, 5, 6, 7, 8}),
            ("♥10 ♥J ♥Q ♥K ♥A", {8, 9, 10, 11, 12}),
        ]
        for cards_str, expect in test_pattern:
            self.assertEqual(Cards(cards_str).rank_indexes(), expect)

    def test_rank_counts(self):
        test_pattern = [
            # カードの組み合わせ, 期待値(各 rank のカード枚数リスト)
            ("♥10 ♥J ♥Q ♥K ♥A", [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1]),
            ("♥6 ♥7 ♥8 ♥9 ♥10", [0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0]),
            ("♥2 ♥3 ♥4 ♥5 ♥6", [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]),
            ("♥2 ♦2 ♥3 ♥4 ♥5", [2, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            ("♥2 ♦2 ♣2 ♥3 ♥4", [3, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            ("♥2 ♦2 ♣2 ♠2 ♥3", [4, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            ("♥2 ♦2 ♣2 ♥3 ♦3", [3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            ("♥2 ♦2 ♥3 ♦3 ♥4", [2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
        ]
        for cards_str, expect in test_pattern:
            self.assertEqual(Cards(cards_str).rank_counts(), expect)

    def test_remove(self):
        # 委譲元のHandクラスでテスト
        pass

    def test_add(self):
        # 委譲元のHandクラスでテスト
        pass

    def test_draw(self):
        # 委譲元のDeckクラスでテスト
        pass

    def test_shuffle(self):
        # 移譲元のDeckクラスでテスト
        pass


class TestDeck(unittest.TestCase):
    suits = ("♠", "♦", "♣", "♥")
    ranks = ("2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A")

    def test_creation(self):
        Deck()
        Deck("♥A ♥K ♥Q ♥J ♥10")

    def test_cards(self):
        # 各カードのリストへの格納順序は問わない。このため、集合に変換して比較する
        self.assertEqual(
            set(Deck().cards()),
            set([Card(s + r) for s in self.suits for r in self.ranks]),
        )

        # 各カードは指定した順序でリストに格納される
        self.assertEqual(
            Deck("♥A ♥K ♥Q ♥J ♥10").cards(),
            [Card("♥A"), Card("♥K"), Card("♥Q"), Card("♥J"), Card("♥10")],
        )

    def test_can_use_len(self):
        self.assertEqual(len(Deck()), 52)
        self.assertEqual(len(Deck("♥A ♥K ♥Q ♥J ♥10")), 5)

    def test_draw(self):
        deck = Deck()

        before_cards = deck.cards()
        card = deck.draw()
        after_cards = deck.cards()

        # カードを引くと、1つへる
        # 引いたカードは、元の要素のどれかと一致し、現在の要素からは削除されている
        self.assertEqual(len(after_cards), len(before_cards) - 1)
        self.assertIn(card, before_cards)
        self.assertNotIn(card, after_cards)

    def test_shuffled(self):
        normal_deck = Deck()
        shuffled_deck = normal_deck.shuffled()

        # シャッフルすると、カードの集合・数は変わらずに、カードの並びだけが変化する
        self.assertEqual(set(normal_deck.cards()), set(shuffled_deck.cards()))
        self.assertEqual(len(normal_deck.cards()), len(shuffled_deck.cards()))
        self.assertNotEqual(normal_deck.cards(), shuffled_deck.cards())


class TestHand(unittest.TestCase):
    def test_creation(self):
        Hand()
        Hand("♥2 ♥4 ♥6 ♥8 ♠10")

    def test_cards(self):
        self.assertEqual(Hand().cards(), [])

        self.assertEqual(
            Hand("♥2 ♥4 ♥6 ♥8 ♠10").cards(),
            [Card("♥2"), Card("♥4"), Card("♥6"), Card("♥8"), Card("♠10")],
        )

    def test_can_use_equal(self):
        self.assertEqual(Hand("♥1 ♥2"), Hand("♥1 ♥2"))
        self.assertNotEqual(Hand("♥1 ♥2"), Hand("♥2 ♥1"))
        self.assertNotEqual(Hand("♥1 ♥2"), Hand("♥1 ♥2 ♥3"))

    def test_can_use_str(self):
        self.assertEqual(str(Hand()), "")
        self.assertEqual(str(Hand("♥2 ♥4 ♥6 ♥8 ♠10")), "♥2 ♥4 ♥6 ♥8 ♠10")

    def test_can_use_len(self):
        self.assertEqual(len(Hand()), 0)
        self.assertEqual(len(Hand("♥2 ♥4 ♥6 ♥8 ♠10")), 5)

    def test_add(self):
        hand = Hand()
        hand.add(Card("♥A"))
        self.assertEqual(hand, Hand("♥A"))

        hand = Hand()
        hand.add(Card("♥A"))
        hand.add(Card("♥K"))
        hand.add(Card("♥Q"))
        hand.add(Card("♥J"))
        hand.add(Card("♥10"))
        self.assertEqual(hand, Hand("♥A ♥K ♥Q ♥J ♥10"))

    def test_remove(self):
        hand = Hand("♥A ♥2 ♥3 ♥4 ♥5")

        # 1枚を捨てる。指定したインデックスのカードが手札から捨てられる
        hand.remove([4])
        self.assertEqual(hand, Hand("♥A ♥2 ♥3 ♥4"))

        # 残りの4枚を捨てる。手札が無くなる
        hand.remove([0, 1, 2, 3])
        self.assertEqual(hand, Hand())

    def test_has_enough_cards(self):
        # 手札が1～4枚ならカード不足
        self.assertFalse(Hand("♥A").has_enough_cards())
        self.assertFalse(Hand("♥A ♥2 ♥3 ♥4").has_enough_cards())

        # 手札が5枚ならカードが足りている
        self.assertTrue(Hand("♥A ♥2 ♥3 ♥4 ♥5").has_enough_cards())

    def test_judge(self):
        test_pattern = [
            # カードの組み合わせ   役の期待値
            ("♥A ♥K ♥Q ♥J ♥10", "Royal Flush"),
            ("♥K ♥Q ♥J ♥10 ♥9", "Straight Flush"),
            ("♥2 ♦2 ♣2 ♠2 ♥4", "Four of a Kind"),
            ("♥2 ♦2 ♣2 ♠4 ♥4", "Full House"),
            ("♥2 ♥4 ♥6 ♥8 ♥10", "Flush"),
            ("♥2 ♥3 ♥4 ♥5 ♠6", "Straight"),
            ("♥2 ♥2 ♥4 ♥5 ♠6", "One Pair"),  # ストレートと誤判定しやすい
            ("♥10 ♥J ♥Q ♥K ♠A", "Straight"),
            ("♥A ♥2 ♥3 ♥4 ♠5", "Straight"),
            ("♥2 ♠2 ♣2 ♥8 ♠10", "Three of a Kind"),
            ("♥2 ♠2 ♥4 ♠4 ♠10", "Two Pair"),
            ("♥2 ♠2 ♥6 ♥8 ♠10", "One Pair"),
            ("♥2 ♥4 ♥6 ♥8 ♠10", "High Card"),
        ]
        for cards_str, expect in test_pattern:
            self.assertEqual(Hand(cards_str).judge(), expect)


class TestDealer(unittest.TestCase):
    def test_deal_cards(self):
        deck = Deck()
        hand = Hand()
        dealer = Dealer()

        # 手札は 0枚 でスタートする
        self.assertEqual(len(hand), 0)

        # 初回のカード配布
        before_deck_len = len(deck)
        dealer.deal_cards(deck, hand)

        # 山札が5枚減って、手札が5枚になる
        self.assertEqual(len(deck), before_deck_len - 5)
        self.assertEqual(len(hand), 5)
        # 手札のカードは、山札内には存在しない
        for card in hand.cards():
            self.assertNotIn(card, deck.cards())

        # 手札から3枚捨てて、手札は2枚になる
        hand.remove([0, 1, 2])
        self.assertEqual(len(hand), 2)

        # 山札から再度カードを配布する
        before_deck_len = len(deck)
        dealer.deal_cards(deck, hand)

        # 山札が3枚減って、手札が5枚に戻る
        self.assertEqual(len(deck), before_deck_len - 3)
        self.assertEqual(len(hand), 5)
        # 手札のカードは、山札内には存在しない
        for card in hand.cards():
            self.assertNotIn(card, deck.cards())


class TestPoker(unittest.TestCase):
    class MockInputWithPrompt:
        """input()のモック(プロンプトを出力しつつ、指定の入力を返す)

        patch("builtins.input", return_value="") でモックすると、プロンプトが出力されずプロンプト自体の検証ができない。
        対策として、専用のモックを用意した
        """

        def __init__(self, return_value):
            self.return_value = return_value

        def __call__(self, prompt):
            print(prompt)  # プロンプトを出力(キー入力後の改行を意図して、改行を付与)
            return self.return_value  # 指定された返り値を返す

    def test_creation(self):
        Poker(Dealer(), Deck().shuffled(), Hand())

    def test_play_without_change(self):
        # 結果を固定するため、山札を指定の並びに設定
        poker = Poker(Dealer(), Deck("♥A ♥K ♥Q ♥J ♥10"), Hand())

        # カード交換時に、何も交換しないよう設定
        # 交換前:♥A ♥K ♥Q ♥J ♥10
        # 交換後:♥A ♥K ♥Q ♥J ♥10
        # (標準入力をモックで置き換えて、空入力を返すようにする)
        with patch("builtins.input", self.MockInputWithPrompt(return_value="")):
            # 標準出力を StringIo に置き換えて、出力をキャプチャする
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                poker.play()

        # 標準出力が期待値と一致すること
        self.assertEqual(
            self.actual_output(mock_stdout),
            #                    初回の手札          交換後の手札        結果
            self.expected_output("♥A ♥K ♥Q ♥J ♥10", "♥A ♥K ♥Q ♥J ♥10", "Royal Flush"),
        )

    def test_play(self):
        # 結果を固定するため、山札を指定の並びに設定
        poker = Poker(Dealer(), Deck("♥A ♥K ♥Q ♥J ♥10 ♠8"), Hand())

        # カード交換時に、インデックス 2 のカードを交換するよう設定
        # 手札から ♥Q を捨てて、山札から ♠8 を補充することになる
        # 交換前:♥A ♥K [♥Q] ♥J ♥10
        # 交換後:♥A ♥K ♥J ♥10 [♠8]
        # (標準入力をモックで置き換えて、"2"を返すようにする)
        with patch("builtins.input", self.MockInputWithPrompt(return_value="2")):
            # 標準出力を StringIo に置き換えて、出力をキャプチャする
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                poker.play()

        # 標準出力が期待値と一致すること
        self.assertEqual(
            self.actual_output(mock_stdout),
            #                    初回の手札          交換後の手札        結果
            self.expected_output("♥A ♥K ♥Q ♥J ♥10", "♥A ♥K ♥J ♥10 ♠8", "High Card"),
        )

    def test_play_shuffle(self):
        poker1 = Poker(Dealer(), Deck().shuffled(), Hand())
        poker2 = Poker(Dealer(), Deck().shuffled(), Hand())

        # カード交換時に、何も交換しないよう設定
        # (標準入力をモックで置き換えて、空入力を返すようにする)
        with patch("builtins.input", self.MockInputWithPrompt(return_value="")):
            # 標準出力を StringIo に置き換えて、出力をキャプチャする
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout1:
                poker1.play()
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout2:
                poker2.play()

        # 最初の手札(標準出力の2行目)が、2回のゲームで異なること
        hand_1st_poker1 = self.actual_output(mock_stdout1)[1]
        hand_1st_poker2 = self.actual_output(mock_stdout2)[1]
        self.assertNotEqual(hand_1st_poker1, hand_1st_poker2)

    def expected_output(self, hand_1st: str, hand_2nd: str, result: str) -> list[str]:
        """標準出力の期待値を、行単位のリストで返す"""
        return [
            "あなたの手札",
            hand_1st,
            "交換するカードの番号(0-4)をスペース区切りで入力: ",
            "交換結果",
            hand_2nd,
            f"結果は {result} です",
        ]

    def actual_output(self, mock_stdout: StringIO) -> list[str]:
        """mock_stdout からキャプチャされた出力を行単位で分割し、リストで返す"""
        return mock_stdout.getvalue().strip().splitlines()


if __name__ == "__main__":
    unittest.main(argv=[""], verbosity=2, exit=False)
