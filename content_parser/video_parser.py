from pathlib import Path


from telethon.client.messages import _MessagesIter
from telethon.tl.types import MessageMediaDocument, Message


from service.convertor import date_convert_to_file_name, file_name_to_date_parse
from config.config import DEFAULT_MEDIA_TYPE


class VideoContentGetter:
    def __init__(self, messages: _MessagesIter) -> None:
        self.__validate_message(messages)

    def __validate_message(self, messages: _MessagesIter) -> None:
        if not isinstance(messages, _MessagesIter):
            raise TypeError(
                '"messages" must be instance "telethon.client.messages._MessageIter" use .iter_messages()')

        self.__messages = messages

    async def __get_media(self, message: Message) -> MessageMediaDocument | None:
        return message.media if isinstance(message.media, MessageMediaDocument) else None

    async def __check_media_type(self, media: MessageMediaDocument) -> bool:
        media_dict_type = media.to_dict()
        for mt in DEFAULT_MEDIA_TYPE:
            if media_dict_type[mt]:
                return True

    async def download(self, last_file_name: str, path_to_save: Path | str, filer: callable) -> str:
        if not isinstance(path_to_save, Path):
            __path_to_save = Path(path_to_save)

        first_file_name = ''

        async for message in self.__messages:
            if not filer(message, file_name_to_date_parse(last_file_name)):
                break

            media = await self.__get_media(message)

            download_videos = []

            if media and await self.__check_media_type(media):
                __file_name = Path(
                    date_convert_to_file_name(message.date, 'mp4')
                )

                if not first_file_name:
                    first_file_name = __file_name

                download_videos.append(__path_to_save / __file_name)

                await message.download_media(__path_to_save / __file_name)

        return str(first_file_name)
