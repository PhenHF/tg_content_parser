import datetime
from telethon.tl.types import Message


def stop_download_by_date(message: Message, last_date: datetime) -> bool:
    return message.date >= last_date
