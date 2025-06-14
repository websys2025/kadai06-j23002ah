# kadai6-1.py

import requests
import pandas as pd

# 取得するデータの種類
# ------------------------------
# 今回は「家計調査（総世帯）消費支出（二人以上の世帯）」のデータを取得します。
# このIDは人口推計以外の統計表です。

APP_ID = "3eaa06acb9f5a187a2e4c0b7765f4e7f28d343a2"
API_URL = "http://api.e-stat.go.jp/rest/3.0/app/json/getStatsData"

params = {
    "appId": APP_ID,                
    "statsDataId": "0003109248",    
    "lang": "J"                     
}

# エンドポイントと機能
# ------------------------------
# エンドポイント: /rest/3.0/app/json/getStatsData
# 機能: 指定した統計表ID（statsDataId）に対応する統計データをJSON形式で取得する

response = requests.get(API_URL, params=params)
data = response.json()

# 使い方
# ------------------------------
# 1. 統計表ID(statsDataId)をe-Statサイトで調べる
# 2. APIキー(APP_ID)をe-Statから取得
# 3. 必要に応じてパラメータを設定し、requests.getでデータを取得
# 4. 統計データ部（VALUE）をpandas.DataFrameに変換
# 5. コードやIDを日本語名称に置換して可読性を高める

values = data['GET_STATS_DATA']['STATISTICAL_DATA']['DATA_INF']['VALUE']
df = pd.DataFrame(values)

meta_info = data['GET_STATS_DATA']['STATISTICAL_DATA']['CLASS_INF']['CLASS_OBJ']

for class_obj in meta_info:
    column_name = '@' + class_obj['@id']
    id_to_name_dict = {}
    if isinstance(class_obj['CLASS'], list):
        for obj in class_obj['CLASS']:
            id_to_name_dict[obj['@code']] = obj['@name']
    else:
        id_to_name_dict[class_obj['CLASS']['@code']] = class_obj['CLASS']['@name']
    if column_name in df.columns:
        df[column_name] = df[column_name].replace(id_to_name_dict)

col_replace_dict = {'@unit': '単位', '$': '値'}
for class_obj in meta_info:
    org_col = '@' + class_obj['@id']
    new_col = class_obj['@name']
    col_replace_dict[org_col] = new_col

new_columns = []
for col in df.columns:
    if col in col_replace_dict:
        new_columns.append(col_replace_dict[col])
    else:
        new_columns.append(col)
df.columns = new_columns

print(df.head())

