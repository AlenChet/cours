import requests


def get_vk_photos(user_id, access_token):
    url = "https://api.vk.com/method/photos.get"
    params = {
        'owner_id': user_id,
        'album_id': 'profile',
        'rev': 1,
        'extended': 1,
        'access_token': access_token,
        'v': '5.131'
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()['response']['items']


def get_yandex_token():
    return input("Введите OAuth токен от Яндекс: ")


def create_folder(folder, oauth_token):
    url = "https://cloud-api.yandex.net/v1/disk/resources"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'OAuth {oauth_token}'
    }
    params = {'path': folder}
    response = requests.put(url, headers=headers, params=params)
    response.raise_for_status()


def upload_yandex(filename, file_url, oauth_token, folder):
    url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'OAuth {oauth_token}'
    }
    params = {
        'path': f'{folder}/{filename}',
        'url': file_url
    }
    response = requests.post(url, headers=headers, params=params)
    response.raise_for_status()

def main():
    user_id = input("Введите id пользователя ВКонтакте: ")
    access_token = input("Введите API токен доступа ВКонтакте: ")
    yandex_token = get_yandex_token()
    folder_name = input("Введите имя папки на Яндекс Диске для сохранения фотографий: ")
    create_folder(folder_name, yandex_token)
    photos = get_vk_photos(user_id, access_token)
    count = 0
    for photo in photos:
        max_size = max(photo['sizes'], key=lambda x: x['width']*x['height'])
        file_url = max_size['url']
        likes = photo['likes']['count']
        filename = f"{likes}.jpg"
        upload_yandex(filename, file_url, yandex_token, folder_name)
        count += 1
        print(f'Фото {count} успешно загружено')
        if count == 5:
            break


if __name__ == '__main__':
    main()
