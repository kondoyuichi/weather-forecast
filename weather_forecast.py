import requests
import json
from datetime import datetime, timedelta
from weather_codes import get_weather_description

# 滋賀県の天気予報API
FORECAST_API_URL = "https://www.jma.go.jp/bosai/forecast/data/forecast/250000.json"

# 対象地域: 0=南部, 1=北部
TARGET_AREA_INDEX = 1

# 天気コード変換はweather_codes.pyのget_weather_description()を使用

def get_weather_data(short_term_weather_series, target_date):
    """天気予報データから天気情報を取得"""
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
    
    return selected_area_name, target_date_weather

def get_rain_data(rain_time_series, target_area_index, target_date):
    print(f"🔍 降水量データ取得開始...")
    
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

def get_temperature_data(temperature_time_series, target_area_index, target_date):
    """
    気温データを取得し、最低気温と最高気温を計算する関数
    
    Args:
        temperature_time_series (dict): 気温時系列データ
        target_area_index (int): 対象地域のインデックス
        
    Returns:
        tuple: (最低気温, 最高気温, 地域名) または None（エラーの場合）
        
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
    
    min_temp = min(target_date_temp_values)  # 最低気温
    max_temp = max(target_date_temp_values)  # 最高気温
    

    print(f"  計算結果: 最低{min_temp}℃, 最高{max_temp}℃")
    print(f"✅ 気温データ取得成功")
    
    return min_temp, max_temp, temp_area_name


def get_weather_forecast():

    """取得する天気予報は、明日"""
    tomorrow_date = datetime.now() + timedelta(days=1)

    """気象庁APIから天気予報データを取得して表示"""
    try:
        response = requests.get(FORECAST_API_URL, timeout=10)
        response.raise_for_status()
        forecast_data = response.json()
        
        """天気予報データから天気情報を取得"""
        short_term_forecast = forecast_data[0]
        
        publishing_office = short_term_forecast["publishingOffice"]
        report_datetime_str = short_term_forecast["reportDatetime"]
        report_datetime = datetime.fromisoformat(report_datetime_str)
        formatted_report_time = f"{report_datetime.year}年{report_datetime.month}月{report_datetime.day}日 {report_datetime.hour}時発表"
        
        short_term_weather_series = short_term_forecast["timeSeries"][0]
        selected_area_name1,tomorrows_weather = get_weather_data(short_term_weather_series, tomorrow_date)

        print(f"✅ 天気データ取得成功: {selected_area_name1} - {tomorrows_weather}")

        """降水量データの取得"""
        rain_time_series = short_term_forecast["timeSeries"][1]
        selected_area_name2, target_date_rain_values = get_rain_data(rain_time_series,TARGET_AREA_INDEX, tomorrow_date)
        print(f"✅ 降水確率データ取得成功: {selected_area_name2} - {target_date_rain_values}")

        """気温データの取得"""
        temperature_time_series = short_term_forecast["timeSeries"][2]
        print(f"  気温データの取得完了")
        
        min_temp, max_temp, temp_area_name = get_temperature_data(temperature_time_series, TARGET_AREA_INDEX, tomorrow_date)
        
        """天気予報の結果を表示"""
        print(f"\n--- 滋賀県の天気予報 ({selected_area_name1}) ---")
        print(f"発表: {publishing_office}")
        print(f"発表時刻: {formatted_report_time}")
        print(f"明日の天気: {tomorrows_weather}")
        # 降水確率をカンマ区切りで表示
        rain_display = ", ".join([f"{value}%" for value in target_date_rain_values])
        print(f"明日の降水確率: {rain_display}")
        print(f"明日の最低気温: {min_temp}℃")
        print(f"明日の最高気温: {max_temp}℃")
        print(f"気温データ提供: {temp_area_name}")

    except requests.exceptions.RequestException as e:
        print(f"通信エラー: インターネット接続またはAPIの状態を確認してください。")
        print(f"詳細: {e}")
    except json.JSONDecodeError as e:
        print(f"データ形式エラー: APIからの応答が不正です。")
        print(f"詳細: {e}")
    except (KeyError, IndexError) as e:
        print(f"データ構造エラー: APIの仕様が変更された可能性があります。")
        print(f"詳細: {e}")
    except ValueError as e:
        print(f"データ処理エラー: {e}")
    except Exception as e:
        print(f"予期せぬエラー: {type(e).__name__}: {e}")
        print(f"問題が続く場合は、プログラムの更新が必要かもしれません。")


if __name__ == "__main__":
    get_weather_forecast() 