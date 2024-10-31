class BaseYandexDiskApi:
    def __init__(self, yandex_config) -> None:
        self._access_token = yandex_config.access_token
        self._prefix_path = yandex_config.prefix_path
