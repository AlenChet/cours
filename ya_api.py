import requests


class YandexDisk:
    def __init__(self, oauth_token):
        self.oauth_token = oauth_token
        self.headers = {
        'Content-Type': "application/json",
        'Authorization': f"OAuth {oauth_token}"
    }

    def create_folder(self, folder):
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        params = {'path': folder}
        response = requests.put(url, headers=self.headers, params=params)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            print(f"Ошибка: {error}")

    def upload_yandex(self, filename, file_url, folder):
        url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        params = {
            'path': f'{folder}/{filename}',
            'url': file_url
        }
        response = requests.post(url, headers=self.headers, params=params)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            print(f"Ошибка: {error}")

    def publish(self, path):
        url = "https://cloud-api.yandex.net/v1/disk/resources/publish"
        params = {'path': path}
        response = requests.put(url, headers=self.headers, params=params)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            print(f"Ошибка: {error}")
        if 'public_url' in response.json():
            return response.json()['public_url']
        else:
            return None