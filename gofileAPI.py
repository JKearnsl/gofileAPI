from json.decoder import JSONDecodeError
import requests


class API:
    """
        Easy Gofile.io SDK
        author: JKearnsl

    """
    def __init__(self):
        self.domain = 'https://api.gofile.io/'
        self.dynamic_domain = 'https://{}.gofile.io/'

    def __check_connect(function_to_decorate):
        """
        Декоратор проверки

        :return:
        """

        def check(self, **kwargs):
            try:
                return function_to_decorate(self, **kwargs)
            except requests.exceptions.ConnectionError as err:
                raise Exception(f"ConnectionError: ошибка подключения | {err}")
            except JSONDecodeError as err:
                raise Exception(f'JSONDecodeError: parser error | {err}')

        return check

    @__check_connect
    def get_server(self):
        """
        Метод используется для получения
        доменного имени 3го уровня свободного
        сервера

        :return: server:str
        """
        req = requests.get(f'{self.domain}getServer').json()
        return req['data']['server'] if req['status'] == 'ok' else req

    @__check_connect
    def uploadFile(self, server: str, file):
        """
        Метод осуществляет загрузку файла на сервер

        :param server: полученный из get_server()
        :param file: файл, который необходимо загрузить
        :return: dict данные
        """

        url = f'{self.dynamic_domain.format(server)}uploadFile'
        req = requests.post(url, files={file.name: file}).json()

        if req['status'] == 'ok':
            del req['data']['info']
            return req['data']
        else:
            return req
