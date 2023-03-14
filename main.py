import json
import os
from pprint import pprint
import requests


class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def check_disk(self):
        """Метод выводит информацию о текущем состоянии яндекс диска"""
        url = 'https://cloud-api.yandex.net:443/v1/disk'
        request = requests.get(url, headers={'Authorization': self.token})
        pprint(request.text)
        return

    def get_link_for_upload(self, file_path):
        """Метод получает ссылку для загрузки файла"""
        file_name = os.path.basename(file_path)
        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        request = requests.get(url,
                               headers={'Authorization': self.token},
                               params={'path': file_name, 'overwrite': True})
        request_to_json = json.loads(request.text)
        return request_to_json['href']

    def upload(self, file_path: str):
        """Метод загружает файлы по полученному url на яндекс диск"""
        get_url = self.get_link_for_upload(file_path)
        response = requests.put(get_url, files={'file': open(file_path, 'rb')})
        print('Response status code of uploading file is ', response.status_code)
        return response.text


if __name__ == '__main__':
    # Получить путь к загружаемому файлу и токен от пользователя
    path_to_file = input()
    token = input()
    uploader = YaUploader(token)
    result = uploader.upload(path_to_file)
