from pathlib import Path


from telethon.client.messages import _MessagesIter


from service.convertor import date_convert_to_file_name
from content_handler.filter import BaseTelegramFilter


# Class for downloading content
class ContentGetter:
    def __init__(self, messages: _MessagesIter, filters: list[BaseTelegramFilter], create_file_name: callable) -> None:
        self.__validate_message(messages)
        self.__validate_filters(filters)
        self.__get_file_name = create_file_name

    def __validate_filters(self, filters: list[BaseTelegramFilter]):
        for f in filters:
            if not isinstance(f, BaseTelegramFilter):
                raise TypeError(
                    "filters must be list[BaseTelegramFilter]"
                )
        self.__filters = filters

    def __validate_message(self, messages: _MessagesIter) -> None:
        if not isinstance(messages, _MessagesIter):
            raise TypeError(
                '"messages" must be instance "telethon.client.messages._MessageIter" use .iter_messages()')

        self.__messages = messages

    async def download(self, path_to_save: Path | str) -> str:
        if not isinstance(path_to_save, Path):
            __path_to_save = Path(path_to_save)

        first_file_name: str

        # Iterate through a list of Messages
        async for message in self.__messages:

            # Iterate through a list of TelegramBaseFilter
            for f in self.__filters:
                ok, file_extension = f.filter(message)
                if not ok:
                    continue

                # TODO Добавить получение функции для создания __file_name из вне
                __file_name = Path(
                    date_convert_to_file_name(message.date, file_extension)
                )

                if not first_file_name:
                    first_file_name = __file_name

                await message.download_media(__path_to_save / __file_name)

        return str(first_file_name)
