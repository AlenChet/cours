import requests
import csv
from datetime import datetime
import json


class Vk_api:
    def __init__(self, user_id, access_token):
        self.user_id = user_id
        self.access_token = access_token

    def get_vk_photos(self):
        url = 'https://api.vk.com/method/photos.get'
        params = {
            'owner_id': self.user_id,
            'album_id': 'profile',
            'rev': 1,
            'extended': 1,
            'access_token': self.access_token,
            'v': '5.131'
        }
        response = requests.get(url, params=params)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            print(f"Ошибка: {error}")

        return response.json()['response']['items']


    def save_photos_to_json(self, file_path):
        photos = self.get_vk_photos()[:5]
        data = []
        for phot, photo in enumerate(photos):
            if phot >=5:
                break
            likes = photo['likes']['count']
            url = photo['sizes'][-1]['url']
            size = photo['sizes'][-1]['type']
            file_name = f"{likes}.jpg"
            data.append({'file_name': file_name, 'size': size})
            # скачиваем фото:
            with open(file_name, 'wb') as file:
                file.write(requests.get(url).content)
        with open(file_path, 'w') as file:
            json.dump(data, file, default=str, ensure_ascii=False, indent=2, separators=(',', ':'))

    def save_photos_to_csv(self, file_path):
        photos = self.get_vk_photos()
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'date', 'likes'])
            for photo in photos:
                photo_id = photo['id']
                date = datetime.fromtimestamp(photo['date'])
                likes = photo['likes']['count']
                writer.writerow([photo_id, date, likes])