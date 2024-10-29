# simple_poker_testing

単体テストの勉強のために作成した、1人用の簡略化ポーカーゲームです。  
テストフレームワークには`unittest`を使用してます。

## ゲームのルール
- プレイヤーは5枚のカードを配られます。
- プレイヤーは、手札から任意の枚数を選び交換できます（交換は1回のみ）。
- 最終的な手札の役によって結果が表示されます。

実際のゲームの流れは、以下の通りです
```
あなたの手札
♣K ♦K ♣8 ♣3 ♦6
交換するカードの番号(0-4)をスペース区切りで入力: 2 3 4
交換結果
♣K ♦K ♦4 ♣A ♦A
結果は Two Pair です
```

## 環境

- **Pythonバージョン**: 3.12.3
- **依存パッケージ**: 標準モジュールのみを使用

## セットアップと実行方法

1. このリポジトリをクローンまたはダウンロードし、`poker.py`と`test.py`が同じフォルダにあることを確認します
2. コマンドラインでフォルダ内に移動し、以下のコマンドでゲームを実行します。
    ```
    > python poker.py
    ```
3. テストを実行するには、以下のコマンドを実行します
    ```
    > python test.py
    ```

## テストコードの設計について
以下の点を工夫(試行錯誤)しました

- ランダム性の除去
    - `Deck`クラスの`shuffled()`メソッドで、山札のシャッフルを選択可能にしました
    - `Deck`クラスのコンストラクタで、山札のカードを自由に設定できるようにしました。例: `Deck("♣K ♦K ♣8 ♣3 ♦6")`
        - ただ、製品コードにテスト用の機能を持たせてしまったのは、良くないと思ってます
- コンソール入力のテスト
    - コンソール入力のモックに`MockInputWithPrompt`を使い、input()によるコンソール入力時に表示される文字列もテストしています

## ライセンス
[MITライセンス](https://github.com/sonokagi/simple_poker_testing/blob/main/LICENSE)