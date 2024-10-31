import requests
from requests import Response

from exception.yadisk_errors import YandexException
from .base_yandex_disk import BaseYandexDiskApi


class YandexDiskInfoGetterMixin:
    def _get_yandex_disk_info(self) -> Response | None:

        __headers = {
            'Authorization': f'OAuth {self._access_token}'
        }

        __params = {
            'path': f"{self._prefix_path}",
            'fields': '_embedded.items.name'
        }

        response = requests.get(
            url='https://cloud-api.yandex.net/v1/disk/resources',
            headers=__headers,
            params=__params
        )

        if response.status_code == 200:
            return response

        else:
            raise YandexException(f"Get info error - {response.json()['message']}\
                                  status code - {response.status_code}")


class YandexDiskFileDeleterMixin:
    def delete_file_from_disk(self, file_name) -> None:

        __headers = {
            'Authorization': f'OAuth {self._access_token}'
        }

        __params = {
            'path': f"{self._prefix_path}/{file_name}",
            'permanently': 'true'
        }

        response = requests.delete(
            url='https://cloud-api.yandex.net/v1/disk/resources',
            headers=__headers,
            params=__params
        )

        if not response.status_code == 204 or not response.status_code == 202:
            raise YandexException(
                f"Deleted error {response.json()}"
            )


class YandexDiskFileUploaderMixin:
    __status_code_messages = {
        201: 'File uploaded successfully',
        202: 'The file was accepted by the server,\
            but has not yet been transferred directly to Yandex Disk',
        'any': f'Uploading error !!!\
                see more: https://yandex.ru/dev/disk-api/doc/ru/reference/upload'
    }

    def __get_upload_url(self, file_name: str) -> str:
        __headers = {
            'Authorization': f'OAuth {self._access_token}'
        }
        __params = {
            'path': f"{self._prefix_path}/{file_name}",
            'overwrite': 'false',
            'fields': 'name'
        }

        response = requests.get(
            url='https://cloud-api.yandex.net/v1/disk/resources/upload',
            headers=__headers,
            params=__params
        )

        if response.status_code == 200:
            return response.json()['href']

        else:
            raise YandexException(response.json()['message'])

    def upload_file(self, file_name: str) -> None:
        try:
            url = self.__get_upload_url(file_name)

            with open(file_name, 'rb') as file:
                response = requests.put(
                    url=url,
                    files={'file': file},
                )

                service_message = self.__status_code_messages.get(
                    response.status_code, None)

                print(
                    service_message if service_message else f"{self.__status_code_messages['any']}\nstatus code - {response.status_code}"
                )

        except YandexException as e:
            print(e)


class YandexDiskFileProcessor(YandexDiskInfoGetterMixin, YandexDiskFileDeleterMixin, YandexDiskFileUploaderMixin, BaseYandexDiskApi):
    def __init__(self, yandex_config) -> None:
        super().__init__(yandex_config)

    @property
    def file_name(self) -> str | None:
        try:
            res_json = self._get_yandex_disk_info().json()
            return res_json['_embedded']['items'][0]['name']

        except YandexException as e:
            print(e)

        except IndexError:
            return None
