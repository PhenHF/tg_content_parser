import datetime
from abc import ABC, abstractmethod

from telethon.tl.types import MessageMediaDocument, Message
from telethon.client.messages import _MessagesIter


from service.content_types import CONTENT_TYPES


class BaseTelegramFilter(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def filter(self, message: Message) -> tuple[bool, str]:
        pass


class TelegramVideoFilter(BaseTelegramFilter):
    def filter(self, message: Message) -> tuple[bool, str]:
        return message.media.video, CONTENT_TYPES["video"]


class TelegramRoundFilter(BaseTelegramFilter):
    def filter(self, message: Message) -> tuple[bool, str]:
        return message.media.round, CONTENT_TYPES["round"]
