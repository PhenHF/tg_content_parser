# import os
# from dataclasses import dataclass


# from dotenv import load_dotenv

# load_dotenv()

# HEADERS = {
#     'Authorization': f'OAuth {os.getenv("ACCESS_TOKEN")}'
# }

# PARAMS = {
#     'path': f'{os.getenv("PATH_TO_UPLOAD_FILE_ON_DISK")}',
#     'overwrite': 'false',
#     'fields': 'name, _embedded.items.path'
# }


# @dataclass
# class YandexDiskRequestParams:
#     path: str = None
#     overwrite: bool = False
#     fields: str = None
