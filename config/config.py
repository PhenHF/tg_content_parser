import os
from dataclasses import dataclass
import datetime


from telethon.tl.types import MessageMediaDocument
from dotenv import load_dotenv


DEFAULT_FILE_NAME = "2024_07_19_18_02_19"

DEFAULT_MEDIA_TYPE = ["video", "round"]

DEFAULT_TELEGRAM_USER_AGENT = {
    'system_version': "4.16.30-vxCUSTOM",
    'device_model': "iPhone 15pro",
}


@dataclass
class TelegramConfig:
    api_hash: str
    api_id: str
    user_agent: dict


@dataclass
class YandexConfig:
    access_token: str
    prefix_path: str


def load_config(user_agent: dict = None) -> TelegramConfig:
    load_dotenv()
    return (
        TelegramConfig(
            api_hash=os.getenv('API_HASH'),
            api_id=os.getenv('API_ID'),
            user_agent=user_agent or DEFAULT_TELEGRAM_USER_AGENT
        ), YandexConfig(
            access_token=os.getenv('ACCESS_TOKEN'),
            prefix_path=os.getenv('PREFIX_PATH')
        )
    )
