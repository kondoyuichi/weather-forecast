"""
気象庁の天気コード（weatherCode）辞書
"""

# 天気コードから天気情報（説明文と絵文字）へのマッピング
WEATHER_DATA = {
    # 100番台: 晴れ系
    "100": {"description": "晴れ", "emoji": "☀️"},
    "101": {"description": "晴れ時々曇り", "emoji": "🌤️"},
    "102": {"description": "晴れ一時雨", "emoji": "🌦️"},
    "103": {"description": "晴れ時々雨", "emoji": "🌦️"},
    "104": {"description": "晴れ一時雪", "emoji": "🌤️"},
    "105": {"description": "晴れ時々雪", "emoji": "🌤️"},
    "106": {"description": "晴れ一時雨後晴れ", "emoji": "🌦️"},
    "107": {"description": "晴れ時々雨後晴れ", "emoji": "🌦️"},
    "108": {"description": "晴れ一時雨後雪", "emoji": "🌦️"},
    "110": {"description": "晴れ後時々曇り", "emoji": "🌤️"},
    "111": {"description": "晴れ後曇り", "emoji": "☀️→☁️"},
    "112": {"description": "晴れ後一時雨", "emoji": "🌦️"},
    "113": {"description": "晴れ後時々雨", "emoji": "🌦️"},
    "114": {"description": "晴れ後雨", "emoji": "☀️→☂️"},
    "115": {"description": "晴れ後一時雪", "emoji": "🌤️"},
    "116": {"description": "晴れ後時々雪", "emoji": "🌤️"},
    "117": {"description": "晴れ後雪", "emoji": "☀️→☃️"},
    "118": {"description": "晴れ後雨後晴れ", "emoji": "🌦️"},
    "119": {"description": "晴れ後雨後雪", "emoji": "🌦️"},
    "120": {"description": "晴れ朝夕一時雨", "emoji": "🌦️"},
    "121": {"description": "晴れ朝のうち一時雨", "emoji": "🌦️"},
    "122": {"description": "晴れ夕方一時雨", "emoji": "🌦️"},
    "123": {"description": "晴れ山沿い雷雨", "emoji": ""},
    "124": {"description": "晴れ山沿い雪", "emoji": "🌤️"},
    "125": {"description": "晴れ午後は雷雨", "emoji": ""},
    "126": {"description": "晴れ昼頃から雨", "emoji": "🌦️"},
    "127": {"description": "晴れ夕方から雨", "emoji": "🌦️"},
    "128": {"description": "晴れ夜は雨", "emoji": "🌦️"},
    "129": {"description": "晴れ夜半から雨", "emoji": "🌦️"},
    "130": {"description": "朝の内霧後晴れ", "emoji": ""},
    "131": {"description": "晴れ明け方霧", "emoji": ""},
    "132": {"description": "晴れ朝夕曇り", "emoji": "🌤️"},
    "140": {"description": "晴れ時々雨で雷を伴う", "emoji": ""},
    "160": {"description": "晴れ一時雪か雨", "emoji": "🌨️"},
    "170": {"description": "晴れ時々雪か雨", "emoji": "🌨️"},
    "181": {"description": "晴れ後雪か雨", "emoji": "🌨️"},
    
    # 200番台: 曇り系
    "200": {"description": "曇り", "emoji": "☁️"},
    "201": {"description": "曇り時々晴れ", "emoji": "⛅"},
    "202": {"description": "曇り一時雨", "emoji": "🌧️"},
    "203": {"description": "曇り時々雨", "emoji": "🌧️"},
    "204": {"description": "曇り一時雪", "emoji": "🌨️"},
    "205": {"description": "曇り時々雪", "emoji": "🌨️"},
    "206": {"description": "曇り一時雨後晴れ", "emoji": "🌦️"},
    "207": {"description": "曇り時々雨後晴れ", "emoji": "🌦️"},
    "208": {"description": "曇り一時雨後雪", "emoji": "🌧️"},
    "209": {"description": "霧", "emoji": "🌫️"},
    "210": {"description": "曇り後時々晴れ", "emoji": "⛅"},
    "211": {"description": "曇り後晴れ", "emoji": "☁️→☀️"},
    "212": {"description": "曇り後一時雨", "emoji": "🌧️"},
    "213": {"description": "曇り後時々雨", "emoji": "🌧️"},
    "214": {"description": "曇り後雨", "emoji": "☁️→☂️"},
    "215": {"description": "曇り後一時雪", "emoji": "🌨️"},
    "216": {"description": "曇り後時々雪", "emoji": "🌨️"},
    "217": {"description": "曇り後雪", "emoji": "☁️→☃️"},
    "218": {"description": "曇り後雨後晴れ", "emoji": "🌦️"},
    "219": {"description": "曇り後雨後雪", "emoji": "🌧️"},
    "220": {"description": "曇り朝夕一時雨", "emoji": "🌧️"},
    "221": {"description": "曇り朝のうち一時雨", "emoji": "🌧️"},
    "222": {"description": "曇り夕方一時雨", "emoji": "🌧️"},
    "223": {"description": "曇り日中時々晴れ", "emoji": "⛅"},
    "224": {"description": "曇り昼頃から雨", "emoji": "🌧️"},
    "225": {"description": "曇り夕方から雨", "emoji": "🌧️"},
    "226": {"description": "曇り夜は雨", "emoji": "🌧️"},
    "227": {"description": "曇り夜半から雨", "emoji": "🌧️"},
    "228": {"description": "曇り昼頃から雪", "emoji": "🌨️"},
    "229": {"description": "曇り夕方から雪", "emoji": "🌨️"},
    "230": {"description": "曇り夜は雪", "emoji": "🌨️"},
    "231": {"description": "曇り海上海岸は霧か霧雨", "emoji": ""},
    "240": {"description": "曇り時々雨で雷を伴う", "emoji": ""},
    "250": {"description": "曇り時々雪で雷を伴う", "emoji": ""},
    "260": {"description": "曇り一時雪か雨", "emoji": "🌨️"},
    "270": {"description": "曇り時々雪か雨", "emoji": "🌨️"},
    "281": {"description": "曇り後雪か雨", "emoji": "🌨️"},
    
    # 300番台: 雨系
    "300": {"description": "雨", "emoji": "☂️"},
    "301": {"description": "雨時々晴れ", "emoji": "🌦️"},
    "302": {"description": "雨時々止む", "emoji": "☂️"},
    "303": {"description": "雨時々雪", "emoji": "🌧️"},
    "304": {"description": "雨雪", "emoji": "☂️"},
    "306": {"description": "大雨", "emoji": "☔️"},
    "307": {"description": "風雨共に強い", "emoji": "☂️"},
    "308": {"description": "雨で暴風を伴う", "emoji": "☂️🌪️"},
    "309": {"description": "雨一時雪", "emoji": "🌧️"},
    "311": {"description": "雨後晴れ", "emoji": "☂️→☀️"},
    "313": {"description": "雨後曇り", "emoji": "☂️→☁️"},
    "314": {"description": "雨後時々雪", "emoji": "🌧️"},
    "315": {"description": "雨後雪", "emoji": "☂️→☃️"},
    "316": {"description": "雨雪後晴れ", "emoji": "🌦️"},
    "317": {"description": "雨雪後曇り", "emoji": "🌧️"},
    "320": {"description": "朝のうち雨後晴れ", "emoji": "🌦️"},
    "321": {"description": "朝のうち雨後曇り", "emoji": "🌧️"},
    "322": {"description": "雨朝晩一時雪", "emoji": "🌧️"},
    "323": {"description": "雨昼頃から晴れ", "emoji": "🌦️"},
    "324": {"description": "雨夕方から晴れ", "emoji": "🌦️"},
    "325": {"description": "雨夜は晴れ", "emoji": "🌦️"},
    "326": {"description": "雨夕方から雪", "emoji": "🌨️"},
    "327": {"description": "雨夜は雪", "emoji": "🌨️"},
    "328": {"description": "雨一時強く降る", "emoji": "☂️"},
    "329": {"description": "雨一時みぞれ", "emoji": "☂️"},
    "340": {"description": "雪か雨", "emoji": "🌨️"},
    "350": {"description": "雨で雷を伴う", "emoji": ""},
    "361": {"description": "雪か雨後晴れ", "emoji": "🌨️"},
    "371": {"description": "雪か雨後曇り", "emoji": "🌨️"},
    
    # 400番台: 雪系
    "400": {"description": "雪", "emoji": "☃️"},
    "401": {"description": "雪時々晴れ", "emoji": "🌨️"},
    "402": {"description": "雪時々止む", "emoji": "☃️"},
    "403": {"description": "雪時々雨", "emoji": "🌨️"},
    "405": {"description": "大雪", "emoji": "☃️"},
    "406": {"description": "風雪強い", "emoji": "🌨️"},
    "407": {"description": "暴風雪", "emoji": "🌨️"},
    "409": {"description": "雪一時雨", "emoji": "🌨️"},
    "411": {"description": "雪後晴れ", "emoji": "☃️→☀️"},
    "413": {"description": "雪後曇り", "emoji": "☃️→☁️"},
    "414": {"description": "雪後雨", "emoji": "☃️→☂️"},
    "420": {"description": "朝のうち雪後晴れ", "emoji": "🌨️"},
    "421": {"description": "朝のうち雪後曇り", "emoji": "🌨️"},
    "422": {"description": "雪昼頃から雨", "emoji": "🌨️"},
    "423": {"description": "雪夕方から雨", "emoji": "🌨️"},
    "424": {"description": "雪夜半から雨", "emoji": "🌨️"},
    "425": {"description": "雪一時強く降る", "emoji": "☃️"},
    "426": {"description": "雪後みぞれ", "emoji": "🌨️"},
    "427": {"description": "雪一時みぞれ", "emoji": "🌨️"},
    "450": {"description": "雪で雷を伴う", "emoji": "☃️⚡"}
}

def get_weather_description(weather_code):
    """
    weatherCodeから天気説明を取得
    
    Args:
        weather_code (str): 気象庁の天気コード
        
    Returns:
        str: 天気の説明文
    """
    weather_data = WEATHER_DATA.get(weather_code)
    if weather_data:
        return weather_data["description"]
    return f"不明な天気コード: {weather_code}"

def get_weather_emoji(weather_code):
    """
    weatherCodeから天気絵文字を取得
    
    Args:
        weather_code (str): 気象庁の天気コード
        
    Returns:
        str: 天気に合う絵文字（マッピングが存在しない場合は空文字）
    """
    weather_data = WEATHER_DATA.get(weather_code)
    if weather_data:
        return weather_data["emoji"]
    return "" 