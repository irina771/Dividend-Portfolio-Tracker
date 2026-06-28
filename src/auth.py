import os
from urllib import response
import requests
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv
# pyrefly: ignore [missing-import]
from dotenv import find_dotenv

load_dotenv(override=True)
TOKEN_URL = "https://api.invertironline.com/token"


def get_access_token():
    payload = {
        "username": os.getenv("USERNAME"),
        "password": os.getenv("PASSWORD"),
        "grant_type": "password"
    }

    response = requests.post(TOKEN_URL, data=payload)
    # print(response.status_code)
    # print(response.text)
    response.raise_for_status()

    data = response.json()

    return {
        "access_token": data["access_token"],
        "refresh_token": data["refresh_token"],
        "expires_in": data["expires_in"]
    }