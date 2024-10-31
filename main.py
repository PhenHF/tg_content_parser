import asyncio


from telethon import TelegramClient


from config.config import load_config, DEFAULT_FILE_NAME
from content_parser.video_parser import VideoContentGetter
from content_handler.video_splicing import VideoSplicer
from yandex_disk_api.disk_file_processing import YandexDiskFileProcessor
from service.filter import stop_download_by_date


def create_client(telegram_config):
    return TelegramClient(
        'anon',
        telegram_config.api_id,
        telegram_config.api_hash,
        **telegram_config.user_agent
    )


async def main(channel_link):
    telegram_config, yandex_config = load_config()
    client = create_client(telegram_config)
    ya_processor = YandexDiskFileProcessor(yandex_config)
    last_file_name = ya_processor.file_name or DEFAULT_FILE_NAME
    async with client:
        chanel = await client.get_entity(channel_link)
        messages = client.iter_messages(chanel)
        vd_getter = VideoContentGetter(messages)
        new_file_name = await vd_getter.download(last_file_name, path_to_save='./videos', filer=stop_download_by_date)

    video_splicer = VideoSplicer('./videos', new_file_name)

    video_splicer.get_full_video()

    # if last_file_name:
    #     ya_processor.delete_file_from_disk(last_file_name)
    ya_processor.upload_file(new_file_name)

if __name__ == '__main__':
    chanel_link = input('Input the channel link: ').strip()
    asyncio.run(main(chanel_link))