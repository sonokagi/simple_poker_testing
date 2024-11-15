# simple_poker_testing

単体テストの勉強のために作成した、1人用の簡略化ポーカーゲームです。  
テストフレームワークには`unittest`を使用してます。  
また、GitHub Actionsを使用して、プルリクエスト時に自動テストの実行・可視化をしています。  
例: [[お試し] GitHub Actions によるテストレポートの動作確認](https://github.com/sonokagi/simple_poker_testing/pull/5)

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
以下の点を工夫しました:
- **ランダム性の除去**
    - テストの再現性を高めるため、`Deck`クラスに以下の機能を追加しました:
        - 山札をシャッフル可能にする`shuffled()`メソッド
        - 任意の初期カードセットを設定できる機能 (例: `Deck("♣K ♦K ♣8 ♣3 ♦6")`)
- **コンソール入力のテスト**
    - コンソール入力をモックするため、`MockInputWithPrompt`を実装。  
      これにより、`input()`による入力時のプロンプト表示内容もテスト対象としています。

## GitHub Actions の設定
このリポジトリではGitHub Actionsを利用して、プルリクエスト時に自動テストと結果の可視化を行っています。

### ワークフローの概要
- **トリガー**: プルリクエスト作成/更新時
- **環境**: Windows環境で、Python 3.12を使用
- **テスト実行方法**: pytestを利用し、unittestで記述したテストを実行。結果をJUnit形式で出力。
- **結果の可視化**: JUnit形式の出力を[publish-unit-test-result-action](https://github.com/EnricoMi/publish-unit-test-result-action)でコメントに反映

ワークフローの設定ファイルはこちらから確認できます: [python-test.yml](https://github.com/sonokagi/simple_poker_testing/blob/main/.github/workflows/python-test.yml)

### テスト結果の例
- **成功例**: [Python unittest #15](https://github.com/sonokagi/simple_poker_testing/actions/runs/11764820983)
- **失敗例**: [Python unittest #14](https://github.com/sonokagi/simple_poker_testing/actions/runs/11764785126)



## ライセンス
このプロジェクトは[MITライセンス](https://github.com/sonokagi/simple_poker_testing/blob/main/LICENSE)のもとで公開されています