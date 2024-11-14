import requests
from bs4 import BeautifulSoup
import pyttsx3
import time

SLEEP_TIME = 1 # プログラムの
# URLを入力
print("読み上げたいWebページのURLを入力してください")
url = input("URL: ")

print("Webページのデータを取得しています")
# スクレイピング
response = requests.get(url)
response.encoding = response.apparent_encoding
# HTMLのみを抜きだす
html = response.text
print("データを取得しました")

# BeautifulSoupオブジェクトの生成
soup = BeautifulSoup(html, "html.parser")

print("読み上げを行います\n")
time.sleep(SLEEP_TIME) # 1秒待つ

# 音声合成エンジンの生成
engine = pyttsx3.init()
lines = list(soup.stripped_strings)
lines_count = len(lines) # 全行数
counter = 1 # 現在の行
for line in lines:
    # 読み上げる文章の表示
    print("{0}  ({1}/{2})".format(line, counter, lines_count))
    # テキストをセット
    engine.say(line)
    # 音量
    engine.setProperty('volume', 0.8)
    # 読み上げスピード
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate)
    # 声の種類のリストを取得
    voices = engine.getProperty('voices')
    # 声の種類
    engine.setProperty('voice', voices[0].id)
    # 合成
    engine.runAndWait()

    counter += 1
print("\n読み上げが終了しました")