# 滋賀県の天気予報取得

滋賀県の天気予報を気象庁のjsonデータから取得し、明日の天気・降水確率・気温を表示するPythonプログラムです。

## 機能

- 滋賀県（北部・南部）の天気予報取得
- 明日の天気、降水確率、最低・最高気温の表示

## インストール

### 1. リポジトリのクローン（またはダウンロード）

```bash
git clone <repository-url>
```

### 2. 依存関係のインストール

```bash
pip install -r requirements.txt
```

## 使用方法

### 基本的な使用方法

```bash
python weather_forecast.py
```

### 実行例

```
🔍 降水量データ取得開始...
  該当日のインデックス: [3, 4, 5, 6]
  該当日の降水確率: ['0', '20', '30', '20']
✅ 降水確率データ取得成功: 北部 - ['0', '20', '30', '20']
🔍 気温データ取得開始...
  該当日のインデックス: [2, 3]
  該当日の気温データ: ['25', '33']
  計算結果: 最低25℃, 最高33℃
✅ 気温データ取得成功

--- 滋賀県の天気予報 (北部) ---
発表: 彦根地方気象台
発表時刻: 2025年7月2日 5時発表
明日の天気: 曇り時々晴れ
明日の降水確率: 0%, 20%, 30%, 20%
明日の最低気温: 25℃
明日の最高気温: 33℃
気温データ提供: 彦根
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
├── weather_forecast.py    # メインプログラム
├── weather_codes.py       # 天気コード辞書モジュール（100+種類）
├── requirements.txt       # 依存関係
├── README.md             # このファイル
└── samples/              # サンプルデータ
    ├── sample1.json      # 気象庁APIレスポンス例1
    ├── sample2.json      # 気象庁APIレスポンス例2
    └── sample3.json      # 気象庁APIレスポンス例3
```


## 気象庁データの利用について

本プロジェクトは、政府標準利用規約に準拠してデータを利用しています。

- [政府標準利用規約(第2.0版)](https://www.digital.go.jp/assets/contents/node/basic_page/field_ref_resources/f7fde41d-ffca-4b2a-9b25-94b8a701a037/a0f187e6/20220706_resources_data_betten_01.pdf)

出典：[気象庁ホームページ](https://www.jma.go.jp/jma/kishou/info/coment.html)

## API情報

このプログラムは気象庁の以下のjsonデータを使用しています。

- **URL**: `https://www.jma.go.jp/bosai/forecast/data/forecast/250000.json`
- **対象地域**: 滋賀県（地域コード: 250000）


## 天気コード情報の出典
- [天気コード一覧 - Weather Information](https://weather.yukigesho.com/code.html) - 気象庁天気コード詳細一覧

**注記**: 天気コード一覧は、気象庁の公式情報が見つからなかったため、第3者の上記サイトを参考にしました。


# 参考情報
- [気象庁公式の天気予報API（？）が発見 ～Twitterの開発者界隈に喜びの声が満ちる - やじうまの杜 - 窓の杜](https://forest.watch.impress.co.jp/docs/serial/yajiuma/1309318.html)
- [気象庁の天気予報JSONファイルをWebAPI的に利用したサンプルアプリ | サンプルアプリ一覧 | あんこエデュケーション](https://anko.education/apps/weather_api)
- [気象庁のAPIと予報区のコード | WebAPI | あんこエデュケーション](https://anko.education/webapi/jma)