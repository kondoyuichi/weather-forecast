# 滋賀県の天気予報取得

滋賀県の天気予報を気象庁のjsonデータから取得し、明日の天気・降水確率・気温を表示するPythonプログラムです。

## 主な機能

### 🌡️ 気温情報・天気予報表示
- **明日の天気予報**: 天気・降水確率・予報気温
- **今日の実測気温(明日の予報との比較)**: 彦根の最高・最低気温（17時以降のみ）
- **Discord Webhook**: 天気予報をDiscordチャンネルに自動通知

## インストール

### 1. リポジトリのクローン

```bash
git clone https://github.com/kondoyuichi/weather-forecast.git
```

### 2. 依存関係のインストール

```bash
pip3 install -r requirements.txt
```

## 使用方法

### 基本的な使用方法

```bash
# コンソールにのみ表示
python3 weather_forecast.py

# Discord通知も送信
python3 weather_forecast.py --discord

# 使用方法を表示
python3 weather_forecast.py --help
```

### Discord通知機能の設定

1. **Discord Webhook URLの取得**
   - Discordで通知したいサーバーの「サーバー設定」→「連携サービス」→「ウェブフック」へアクセス
   - 「新しいウェブフック」をクリック
   - ウェブフック名を設定（例：「天気予報Bot」）
   - 通知するチャンネルを選択
   - 「ウェブフックURLをコピー」でURLを取得

2. **.envファイル**
   - `DISCORD_WEBHOOK_URL`変数に取得したURLを設定
   ```python
   # Discord Webhook URL設定
   DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/あなたのWebhookURL"
   ```

3. **実行**
   ```bash
   python3 weather_forecast.py --discord
   ```

### テスト用時刻設定

`weather_forecast.py`の`TEST_HOUR`変数を編集：

```python
# 15時前の動作をテスト
TEST_HOUR = 14

# 15時後の動作をテスト 
TEST_HOUR = 16

# 実際の時刻を使用
TEST_HOUR = None
```

## 実行例

### 15時後の実行例

```
🕐 実行時刻: 15:40
🌅 15時以降の実行です。当日の気温との比較を表示します。
🔍 天気データ取得開始...
  該当日のインデックス: 1
✅ 天気データ取得成功: 北部 - 曇り時々晴れ
🔍 降水確率データ取得開始...
  該当日のインデックス: [2, 3, 4, 5]
  該当日の降水確率: ['10', '20', '30', '30']
✅ 降水確率データ取得成功: 北部 - ['10', '20', '30', '30']
🔍 気温データ取得開始...
  該当日のインデックス: [2, 3]
  該当日の気温データ: ['27', '33']
  計算結果: 最低27.0℃, 最高33.0℃
✅ 気温データ取得成功
🔍 今日の実際の気温データ取得開始...
  彦根の今日の実績（HTML取得）: 最高34.0℃、最低25.3℃
✅ 今日の実績気温取得成功（HTML）

============================================================
🌡️  滋賀県の気温情報・天気予報 (北部)
============================================================
📅 発表: 彦根地方気象台
📅 発表時刻: 2025年7月7日 11時発表

📊 今日の実際の気温（彦根）
   最高気温: 34.0℃
   最低気温: 25.3℃

🔮 明日の天気予報
   天気: 曇り時々晴れ
   降水確率: 10%, 20%, 30%, 30%
   予報最高気温: 33.0℃ (前日比: -1.0℃)
   予報最低気温: 27.0℃ (前日比: +1.7℃)

============================================================

📱 Discord通知を送信しています...
📩 Discord通知送信中...
✅ Discord通知送信成功
✅ Discord通知が正常に送信されました
```

**Discordに表示される内容例：**
```
7月8日の天気予報（北部）
⛅ 曇り時々晴れ
降水確率：20% / 30%
最高気温：33.0℃ (前日比-1.0℃)
最低気温：27.0℃ (前日比+1.7℃)

[気象庁の天気予報](<https://www.jma.go.jp/bosai/forecast/#area_type=offices&area_code=250000>)
[おうみ発630の天気予報(平日)](<https://www.nhk.jp/p/omi630/ts/8RG6LZ736N/list/>)
```

## 設定

### 対象地域の変更
`weather_forecast.py`の以下の部分を編集することで、対象地域を変更できます：
```python
# 滋賀の対象地域: 0=南部, 1=北部
TARGET_AREA_INDEX = 1  # 0に変更すると南部の天気予報を取得
```

## ファイル構成

```
folder_name/
├── weather_forecast.py           # メインプログラム
├── weather_codes.py              # 天気コード辞書モジュール
├── requirements.txt              # 依存関係
├── README.md                     # このファイル
├── samples/                      # サンプルデータ
│   ├── sample1.json             # 気象庁APIレスポンス例1
│   ├── sample2.json             # 気象庁APIレスポンス例2
│   └── sample3.json             # 気象庁APIレスポンス例3
```

## 気象庁データの利用について

本プロジェクトは、政府標準利用規約に準拠してデータを利用しています。

- [政府標準利用規約(第2.0版)](https://www.digital.go.jp/assets/contents/node/basic_page/field_ref_resources/f7fde41d-ffca-4b2a-9b25-94b8a701a037/a0f187e6/20220706_resources_data_betten_01.pdf)

出典：[気象庁ホームページ](https://www.jma.go.jp/jma/kishou/info/coment.html)

## API情報

このプログラムは気象庁の以下のjsonデータを使用しています。

- **URL**: `https://www.jma.go.jp/bosai/forecast/data/forecast/250000.json`
- **対象地域**: 滋賀県（地域コード: 250000）

### 気象庁の観測データ

- **URL**: `https://www.data.jma.go.jp/obd/stats/data/mdrr/synopday/data1s.html`



## 天気コード情報の出典

- [天気コード一覧 - Weather Information](https://weather.yukigesho.com/code.html) - 気象庁天気コード詳細一覧

**注記**: 天気コード一覧は、気象庁の公式情報が見つからなかったため、第3者の上記サイトを参考にしました。

# 参考情報

- [気象庁公式の天気予報API（？）が発見 ～Twitterの開発者界隈に喜びの声が満ちる - やじうまの杜 - 窓の杜](https://forest.watch.impress.co.jp/docs/serial/yajiuma/1309318.html)
- [気象庁の天気予報JSONファイルをWebAPI的に利用したサンプルアプリ | サンプルアプリ一覧 | あんこエデュケーション](https://anko.education/apps/weather_api)
- [気象庁のAPIと予報区のコード | WebAPI | あんこエデュケーション](https://anko.education/webapi/jma)
