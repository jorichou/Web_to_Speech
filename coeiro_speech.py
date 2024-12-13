import requests
from bs4 import BeautifulSoup
import time
import os
import json
import ffmpeg
import save_speakers as sasp

SLEEP_TIME = 1 # プログラムの
API_SERVER = "http://127.0.0.1:50032"
OUTPUT_FILE = "audio.wav"
SPEAKER_UUID = "3c37646f-3881-5374-2a83-149267990abc"
SPEAKERS_FILE = "speakers.json"
STYLE_ID = 0

def synthesis(text: str):
    """
    文字列を音声化する
    """
    query = {
        "speakerUuid": SPEAKER_UUID,
        "styleId": STYLE_ID,
        "text": text,
        "speedScale": 1.0,
        "volumeScale": 1.0,
        "prosodyDetail": [],
        "pitchScale": 0.0,
        "intonationScale": 1.0,
        "prePhonemeLength": 0.1,
        "postPhonemeLength": 0.5,
        "outputSamplingRate": 24000,
    }

    # 音声合成を実行
    response = requests.post(
        f"{API_SERVER}/v1/synthesis",
        headers={"Content-Type": "application/json"},
        data=json.dumps(query)
    )
    response.raise_for_status()

    return response.content


def append_audio(audio1: str, audio2: str):
    """
    audio1の後ろにaudio2を結合する
    """
    old_file = "old.wav"
    os.rename(audio1, old_file)
    (
        ffmpeg.concat(ffmpeg.input(old_file), ffmpeg.input(audio2), v=0, a=1)
        .output(audio1)
        .run()
    )
    os.remove(old_file)


if __name__ == "__main__":
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

    # 使用できる声を取得
    sasp.save_speakers()
    with open(SPEAKERS_FILE) as f:
        speakers = json.load(f)

    # 使用する声を選択
    print("使用したい声を選んでください")
    print("キャラクター名: ID")
    for speaker in speakers:
        print("{0}: {1}".format(speaker["speakerName"], speaker["styles"]["styleId"]))

    STYLE_ID = input(input("ID: "))

    print("読み上げを行います\n")
    time.sleep(SLEEP_TIME) # 1秒待つ
    count = 0
    lines = list(soup.stripped_strings)
    for line in lines:
        # テキストの音声化
        audio = synthesis(line)

        if count == 0:
            with open(OUTPUT_FILE, "wb") as f_temp:
                f_temp.write(audio)
        else:
            temp_file = "temp.wav"
            with open(temp_file, "wb") as f_temp:
                f_temp.write(audio)
            append_audio(OUTPUT_FILE, temp_file)
            os.remove(temp_file)

        count += 1