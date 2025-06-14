
#参照するオープンデータについて
#データ名: 気象庁 天気予報データ
#概要: 日本全国の天気予報、気温、降水確率などの防災情報をJSON形式で提供している
        #オープンデータです。APIキーなどの認証は不要で、誰でも自由に利用できます。
        #今回は、指定した地域の天気予報を取得します。
#公式情報: https://www.jma.go.jp/jma/kishou/know/bosai/jma-json.html

#エンドポイントと機能
#エンドポイントURL: https://www.jma.go.jp/bosai/forecast/data/forecast/{area_code}.json
#機能:
  #{area_code} に地方、都道府県、または地域のエリアコードを指定することで、
    #該当地域の天気予報データをJSON形式で取得できます。

#プログラムの使い方
#下記コードの `AREA_CODE` を、予報を知りたい地域のコードに変更します。
#主要なコードの例:
   #"130000": 東京都
   #"270000": 大阪府
   #"016000": 北海道（札幌）
   #"400000": 福岡県
#コマンドラインで `python kadai6-2.py` を実行します。

import requests
import json
from datetime import datetime

AREA_CODE = "130000"

url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{AREA_CODE}.json"

print(f"気象庁から天気予報データを取得します... (エリアコード: {AREA_CODE})")

try:
    response = requests.get(url)
    response.raise_for_status()

    response.encoding = 'utf-8-sig'
    data = response.json()

    print("データの取得に成功しました。")

    forecast_data = data[0]
    
    publishing_office = forecast_data["publishingOffice"]
    report_datetime_str = forecast_data["reportDatetime"]
    report_datetime = datetime.fromisoformat(report_datetime_str).strftime('%Y年%m月%d日 %H:%M')

    time_series = forecast_data["timeSeries"]
    
    weather_info = time_series[0]
    precip_info = time_series[1]
    temp_info = time_series[2]

    area_name = weather_info["areas"][0]["area"]["name"]

    print("\n--- 取得した天気予報 ---")
    print(f"対象地域: {area_name} ({publishing_office})")
    print(f"発表時刻: {report_datetime}")
    print("--------------------------")

    for i in range(2):
        date_str = weather_info["timeDefines"][i]
        date_obj = datetime.fromisoformat(date_str)
        date_formatted = date_obj.strftime('%Y年%m月%d日')
        day_label = "今日" if i == 0 else "明日"
        
        weather = weather_info["areas"][0]["weathers"][i]
        
        precip_periods = precip_info["timeDefines"]
        precip_values = precip_info["areas"][0]["pops"]
        precip_text = ", ".join([f"{p_time[11:16]}〜: {p_val}%" for p_time, p_val in zip(precip_periods[i*4:(i+1)*4], precip_values[i*4:(i+1)*4])])
        
        min_temp = temp_info["areas"][0]["temps"][i*2]
        max_temp = temp_info["areas"][0]["temps"][i*2 + 1]
        temp_text = f"最低 {min_temp}℃ / 最高 {max_temp}℃"

        print(f"\n■ {date_formatted} ({day_label})")
        print(f"  天気: {weather}")
        print(f"  気温: {temp_text}")
        print(f"  降水確率: {precip_text}")

except requests.exceptions.RequestException as e:
    print(f"APIへのリクエスト中にエラーが発生しました: {e}")
except json.JSONDecodeError as e:
    print(f"取得したデータの形式が正しくありません (JSONエラー): {e}")
except (KeyError, IndexError) as e:
    print(f"取得したデータの構造が予期したものと異なります。エリアコードが正しいか確認してください。")
except Exception as e:
    print(f"予期せぬエラーが発生しました: {e}")
