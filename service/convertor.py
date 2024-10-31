import datetime
from telethon.tl.types import Message


def date_convert_to_file_name(date: datetime, file_extension: str) -> str:
    return f"{date.strftime('%Y_%m_%d_%H_%M_%S')}.{file_extension}"


def file_name_to_date_parse(file_name: str) -> datetime:
    date = file_name.split('_')
    date[-1] = date[-1].replace('.mp4', '')
    return datetime.datetime(*map(int, date), tzinfo=datetime.timezone.utc)
