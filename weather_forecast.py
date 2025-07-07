import requests
import json
import os
import warnings
from datetime import datetime, timedelta
from weather_codes import get_weather_description, get_weather_emoji
import re
from dotenv import load_dotenv

# SSL警告を非表示にする（実際の通信には影響しない）
warnings.filterwarnings('ignore', message='urllib3 v2 only supports OpenSSL 1.1.1+.*')

# .envファイルから環境変数を読み込み
load_dotenv()

# Discord Webhook URL設定
DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL', '')

# 滋賀県の天気予報API
FORECAST_API_URL = "https://www.jma.go.jp/bosai/forecast/data/forecast/250000.json"

# 対象地域: 0=南部, 1=北部
TARGET_AREA_INDEX = 1

# 観測データHTML（毎日の全国データ）
OBSERVATION_HTML_URL = "https://www.data.jma.go.jp/obd/stats/data/mdrr/synopday/data1s.html"

# テスト用時刻設定（None=実際の時刻を使用、数値=指定時刻でテスト）
TEST_HOUR = None  # 例: 14で15時前をテスト、16で15時後をテスト

# Discord通知機能
def send_discord_notification(message):
    """
    Discord Webhookを使用してメッセージを送信する。
    
    Args:
        message (str): 送信するメッセージ
        
    Returns:
        bool: 送信成功時True、失敗時False
    """
    if not DISCORD_WEBHOOK_URL:
        print("⚠️  Discord Webhook URLが設定されていません。")
        return False
    
    try:
        print("📩 Discord通知送信中...")
        
        # Discord Webhookに送信するデータ
        data = {
            "content": message,
            "username": "滋賀県の天気予報"  # ボットの表示名
        }
        
        response = requests.post(
            DISCORD_WEBHOOK_URL,
            json=data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 204:
            print("✅ Discord通知送信成功")
            return True
        else:
            print(f"❌ Discord通知送信失敗: ステータスコード {response.status_code}")
            print(f"レスポンス: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Discord通知送信エラー: {e}")
        return False
    except Exception as e:
        print(f"❌ Discord通知処理エラー: {e}")
        return False



# 天気予報データから指定日の天気情報を取得
def get_weather_data(short_term_weather_series, target_date):
    """
    天気予報データから指定日の天気情報を取得する。
    
    Args:
        short_term_weather_series (dict): 短期予報の時系列データ
        target_date (datetime): 取得対象の日付
        
    Returns:
        tuple: (地域名, 天気の文字列, 天気コード)
    """

    print(f"🔍 天気データ取得開始...")

    short_term_weather_time_defines = short_term_weather_series["timeDefines"]

    selected_weather_area = short_term_weather_series["areas"][TARGET_AREA_INDEX]
    selected_area_name = selected_weather_area["area"]["name"]

    target_date_index = None
    for i, time_str in enumerate(short_term_weather_time_defines):
        time_obj = datetime.fromisoformat(time_str)
        if time_obj.date() == target_date.date():
            target_date_index = i
            break
    
    if target_date_index is None:
        raise ValueError(f"該当日 ({target_date.date()})のデータが見つかりません")
    
    print(f"  該当日のインデックス: {target_date_index}")
    
    target_date_weather_code = selected_weather_area["weatherCodes"][target_date_index]
    target_date_weather = get_weather_description(target_date_weather_code)
    
    return selected_area_name, target_date_weather, target_date_weather_code

# 降水確率データを取得
def get_rain_data(rain_time_series, target_area_index, target_date):
    """
    降水確率データを取得する。
    
    Args:
        rain_time_series (dict): 降水確率時系列データ
        target_area_index (int): 対象地域のインデックス
        target_date (datetime): 取得対象の日付
        
    Returns:
        tuple: (地域名, 降水確率のリスト)
    """
    print(f"🔍 降水確率データ取得開始...")
    
    # 時系列データと地域データを分けて取得
    rain_time_defines = rain_time_series["timeDefines"]
    selected_rain_area = rain_time_series["areas"][target_area_index]
    selected_area_name = selected_rain_area["area"]["name"]

    target_date_index = []
    for i, time_str in enumerate(rain_time_defines):
        time_obj = datetime.fromisoformat(time_str)
        if time_obj.date() == target_date.date():
            target_date_index.append(i)

    if not target_date_index:
        raise ValueError(f"該当日 ({target_date.date()})のデータが見つかりません")

    print(f"  該当日のインデックス: {target_date_index}")

    target_date_rain_values = []
    for index in target_date_index:
        target_date_rain_values.append(selected_rain_area["pops"][index])

    print(f"  該当日の降水確率: {target_date_rain_values}")

    return selected_area_name, target_date_rain_values

# 気温データを取得し、最低気温と最高気温を計算
def get_temperature_data(temperature_time_series, target_area_index, target_date):
    """
    気温データを取得し、最低気温と最高気温を計算する。
    
    Args:
        temperature_time_series (dict): 気温時系列データ
        target_area_index (int): 対象地域のインデックス
        target_date (datetime): 取得対象の日付
        
    Returns:
        tuple: (最低気温, 最高気温, 地域名)
        
    Raises:
        ValueError: 気温データの取得に失敗した場合
    """
    print(f"🔍 気温データ取得開始...")

    temp_time_defines = temperature_time_series["timeDefines"]
    target_date_index = []
    for i, time_str in enumerate(temp_time_defines):
        time_obj = datetime.fromisoformat(time_str)
        if time_obj.date() == target_date.date():
            target_date_index.append(i)

    if not target_date_index:
        raise ValueError(f"該当日 ({target_date.date()})のデータが見つかりません")
    
    print(f"  該当日のインデックス: {target_date_index}")

    target_area_temps = temperature_time_series["areas"][target_area_index]["temps"]
    temp_area_name = temperature_time_series["areas"][target_area_index]["area"]["name"]

    target_date_temp_values = []
    for i in target_date_index:
        target_date_temp_values.append(target_area_temps[i])

    print(f"  該当日の気温データ: {target_date_temp_values}")
    
    # 文字列を数値に変換してから最低・最高を計算
    numeric_temp_values = [float(temp) for temp in target_date_temp_values]
    min_temp = min(numeric_temp_values)  # 最低気温
    max_temp = max(numeric_temp_values)  # 最高気温
    
    print(f"  計算結果: 最低{min_temp}℃, 最高{max_temp}℃")
    print(f"✅ 気温データ取得成功")
    
    return min_temp, max_temp, temp_area_name

# 気象庁観測データから彦根の今日の実際の気温を取得
def get_today_actual_temperature():
    """
    気象庁の観測データWebページから彦根の今日の実際の気温を取得する。
    
    HTMLページをスクレイピングして、彦根の最高気温と最低気温を抽出する。
    データが取得できない場合は(None, None)を返す。
    
    Returns:
        tuple: 成功時は(最高気温, 最低気温)のfloat値、失敗時は(None, None)
    
    Raises:
        requests.exceptions.RequestException: HTTPリクエストエラー
        Exception: その他の処理エラー
    """
    print("🔍 今日の実際の気温データ取得開始...")
    
    try:
        response = requests.get(OBSERVATION_HTML_URL, timeout=15)
        response.raise_for_status()
        response.encoding = 'utf-8'  # 文字エンコーディングを明示的に設定
        html_content = response.text
        
        # 彦根の行を検索
        hikone_pattern = r'彦根.*?(\d+\.\d+)\].*?(\d+:\d+)\].*?(\d+\.\d+)\].*?(\d+:\d+)\].*?(\d+\.\d+)\]'
        matches = re.search(hikone_pattern, html_content)
        
        if matches:
            max_temp = float(matches.group(3)) # 最高気温
            min_temp = float(matches.group(5)) # 最低気温
            
            print(f"  彦根の今日の実績（HTML取得）: 最高{max_temp}℃、最低{min_temp}℃")
            print("✅ 今日の実績気温取得成功（HTML）")
            
            return max_temp, min_temp
        else:
            # 最終フォールバック
            print("⚠️  観測データの解析に失敗しました。")
            return None, None
            
    except requests.exceptions.RequestException as e:
        print(f"⚠️  観測データ取得エラー: {e}")
        return None, None
    except Exception as e:
        print(f"⚠️  観測データ処理エラー: {e}")
        return None, None



# Discord用メッセージフォーマット関数
def format_discord_message(selected_area_name, publishing_office, formatted_report_time, 
                          is_after_17, today_max_actual, today_min_actual,
                          tomorrows_weather, target_date_rain_values, 
                          tomorrow_max_forecast, tomorrow_min_forecast,
                          max_diff_str, min_diff_str, weather_code):
    """
    天気予報データをDiscord用のメッセージにフォーマットする。
    
    Args:
        selected_area_name (str): 地域名
        publishing_office (str): 発表元
        formatted_report_time (str): 発表時刻
        is_after_15 (bool): 15時以降かどうか
        today_max_actual (float): 今日の実際の最高気温
        today_min_actual (float): 今日の実際の最低気温
        tomorrows_weather (str): 明日の天気
        target_date_rain_values (list): 降水確率のリスト
        tomorrow_max_forecast (float): 明日の予報最高気温
        tomorrow_min_forecast (float): 明日の予報最低気温
        max_diff_str (str): 最高気温の前日比
        min_diff_str (str): 最低気温の前日比
        weather_code (str): 天気コード
        
    Returns:
        str: Discord用フォーマット済みメッセージ
    """
    # 明日の日付を取得
    tomorrow_date = datetime.now() + timedelta(days=1)
    date_str = f"{tomorrow_date.month}月{tomorrow_date.day}日"
    
    # 天気に合う絵文字を取得
    weather_emoji = get_weather_emoji(weather_code)
    weather_line = f"{weather_emoji} {tomorrows_weather}"
    
    # 降水確率を午前・午後のみに変更
    # 通常、気象庁のデータは [0-6時, 6-12時, 12-18時, 18-24時] の順で提供される
    rain_6to12 = ""
    rain_12to18 = ""
    
    if len(target_date_rain_values) >= 3:
        # 午前(6-12時)と午後(12-18時)を取得
        rain_6to12 = target_date_rain_values[1]  # 6-12時
        rain_12to18 = target_date_rain_values[2]  # 12-18時
    else:
        # データが不十分な場合は利用可能なデータを使用
        print("⚠️ 降水確率データが不十分です。")
    
    # メッセージを新しいフォーマットで作成
    message = f"""## {date_str}の天気予報（{selected_area_name}）
- {weather_line}
- 降水確率：{rain_6to12}% / {rain_12to18}%
- 最高気温：{tomorrow_max_forecast}℃ (前日比{max_diff_str})
- 最低気温：{tomorrow_min_forecast}℃ (前日比{min_diff_str})

[気象庁の天気予報](<https://www.jma.go.jp/bosai/forecast/#area_type=offices&area_code=250000>)
[おうみ発630の天気予報(平日のみ)](<https://www.nhk.jp/p/omi630/ts/8RG6LZ736N/list/>)"""
    
    return message

# 天気予報と今日の実績気温、前日比を取得して表示
def get_weather_forecast_with_comparison(send_to_discord=False):

    # 実行時刻をチェック（テスト用時刻が設定されている場合はそれを使用）
    current_time = datetime.now()
    test_hour = TEST_HOUR
    
    if test_hour is not None:
        print(f"🧪 テストモード: 仮想時刻 {test_hour}:00")
        current_hour = test_hour
    else:
        print(f"🕐 実行時刻: {current_time.strftime('%H:%M')}")
        current_hour = current_time.hour
    
    # 15時以降の実行かどうかを判定
    is_after_15 = current_hour >= 15
    
    if is_after_15:
        print("🌅 15時以降の実行です。当日の気温との比較を表示します。")
    else:
        print("🌅 15時前の実行です。当日の気温との比較は表示しません。")

    tomorrow_date = datetime.now() + timedelta(days=1)
    
    # 明日の予報を取得
    try:
        response = requests.get(FORECAST_API_URL, timeout=10)
        response.raise_for_status()
        forecast_data = response.json()
        
        # 天気予報データから情報を取得
        short_term_forecast = forecast_data[0]
        
        publishing_office = short_term_forecast["publishingOffice"]
        report_datetime_str = short_term_forecast["reportDatetime"]
        report_datetime = datetime.fromisoformat(report_datetime_str)
        formatted_report_time = f"{report_datetime.year}年{report_datetime.month}月{report_datetime.day}日 {report_datetime.hour}時発表"
        
        # 天気情報
        short_term_weather_series = short_term_forecast["timeSeries"][0]
        selected_area_name1, tomorrows_weather, weather_code = get_weather_data(short_term_weather_series, tomorrow_date)
        print(f"✅ 天気データ取得成功: {selected_area_name1} - {tomorrows_weather}")

        # 降水確率
        rain_time_series = short_term_forecast["timeSeries"][1]
        selected_area_name2, target_date_rain_values = get_rain_data(rain_time_series, TARGET_AREA_INDEX, tomorrow_date)
        print(f"✅ 降水確率データ取得成功: {selected_area_name2} - {target_date_rain_values}")

        # 明日の気温予報
        temperature_time_series = short_term_forecast["timeSeries"][2]
        tomorrow_min_forecast, tomorrow_max_forecast, temp_area_name = get_temperature_data(temperature_time_series, TARGET_AREA_INDEX, tomorrow_date)
        
        # 前日比計算（今日の実測データが取得できた場合のみ）
        max_diff_str = "データなし"
        min_diff_str = "データなし"
        today_max_actual = None
        today_min_actual = None

        # 15時以降の場合、当日の気温を取得し、明日の予報と前日比を計算する
        if is_after_15:
            # 今日の実際の気温を取得
            today_max_actual, today_min_actual = get_today_actual_temperature()
            
            if today_max_actual is not None and today_min_actual is not None:
                # 前日比を直接計算（明日の予報 - 今日の実績）
                max_diff = float(tomorrow_max_forecast) - float(today_max_actual)
                min_diff = float(tomorrow_min_forecast) - float(today_min_actual)
                
                # 前日比を読みやすい形式に変換
                def format_diff(diff):
                    if diff > 0:
                        return f"+{diff:.1f}℃"
                    elif diff < 0:
                        return f"{diff:.1f}℃"
                    else:
                        return "±0℃"
                
                max_diff_str = format_diff(max_diff)
                min_diff_str = format_diff(min_diff)
        else:
            print("🌅 15時前の実行です。当日の気温との比較は表示しません。")
        
        # 結果表示
        print(f"\n" + "="*60)
        print(f"🌡️  滋賀県の気温情報・天気予報 ({selected_area_name1})")
        print(f"="*60)
        print(f"📅 発表: {publishing_office}")
        print(f"📅 発表時刻: {formatted_report_time}")
        print("")
        
        print("📊 今日の実際の気温（彦根）")
        if is_after_15:
            if today_max_actual is not None and today_min_actual is not None:
                print(f"   最高気温: {today_max_actual}℃")
                print(f"   最低気温: {today_min_actual}℃")
            else:
                print("   ⚠️  今日の実測データが取得できませんでした")
        else:
            print("   ⚠️  15時前の実行のため、データなし")
        print("")
        
        print("🔮 明日の天気予報")
        print(f"   天気: {tomorrows_weather}")
        rain_display = ", ".join([f"{value}%" for value in target_date_rain_values])
        print(f"   降水確率: {rain_display}")
        print(f"   予報最高気温: {tomorrow_max_forecast}℃ (前日比: {max_diff_str})")
        print(f"   予報最低気温: {tomorrow_min_forecast}℃ (前日比: {min_diff_str})")
        print("")
        
        print(f"="*60)
        
        # Discord通知（オプション）
        if send_to_discord:
            print("\n📱 Discord通知を送信しています...")
            discord_message = format_discord_message(
                selected_area_name1, publishing_office, formatted_report_time,
                is_after_15, today_max_actual, today_min_actual,
                tomorrows_weather, target_date_rain_values,
                tomorrow_max_forecast, tomorrow_min_forecast,
                max_diff_str, min_diff_str, weather_code
            )
            
            success = send_discord_notification(discord_message)
            if success:
                print("✅ Discord通知が正常に送信されました")
            else:
                print("❌ Discord通知の送信に失敗しました")

    except requests.exceptions.RequestException as e:
        print(f"❌ 通信エラー: インターネット接続またはAPIの状態を確認してください。")
        print(f"詳細: {e}")
    except json.JSONDecodeError as e:
        print(f"❌ データ形式エラー: APIからの応答が不正です。")
        print(f"詳細: {e}")
    except (KeyError, IndexError) as e:
        print(f"❌ データ構造エラー: APIの仕様が変更された可能性があります。")
        print(f"詳細: {e}")
    except ValueError as e:
        print(f"❌ データ処理エラー: {e}")
    except Exception as e:
        print(f"❌ 予期せぬエラー: {type(e).__name__}: {e}")
        print(f"問題が続く場合は、プログラムの更新が必要かもしれません。")

def show_usage():
    """
    使用方法を表示する関数
    """
    print("🔧 使用方法:")
    print("1. コンソールにのみ表示: python3 weather_forecast.py")
    print("2. Discord通知も送信: python3 weather_forecast.py --discord")
    print("3. Discord通知テスト: python3 test_discord.py")
    print("")
    print("📋 Discord通知を使用する場合の設定:")
    print("1. DiscordでWebhook URLを取得")
    print("2. .envファイルにDISCORD_WEBHOOK_URL=あなたのWebhookURLを設定")
    print("3. --discordオプションを付けて実行")

if __name__ == "__main__":
    import sys
    
    # コマンドライン引数をチェック
    if len(sys.argv) > 1:
        if sys.argv[1] == "--discord":
            # Discord通知あり
            get_weather_forecast_with_comparison(send_to_discord=True)
        elif sys.argv[1] == "--help" or sys.argv[1] == "-h":
            # 使用方法を表示
            show_usage()
        else:
            print("❌ 無効な引数です。")
            show_usage()
    else:
        # Discord通知なし（デフォルト）
        get_weather_forecast_with_comparison(send_to_discord=False) 