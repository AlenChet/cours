from vk_api import Vk_api
from ya_api import YandexDisk


if __name__=='__main__':
    user_id = input("Введите id пользователя ВКонтакте: ")
    access_token = input("Введите VK token: ")
    vk_api = Vk_api(user_id, access_token)

    yandex_token = input("Введите oauth-токен от Яндекс: ")
    yandex_api = YandexDisk(yandex_token)

    folder_name = input("Введите имя папки на Яндекс Диске для сохранения фотографий: ")
    yandex_api.create_folder(folder_name)

    photos = vk_api.get_vk_photos()
    count = 0

    for photo in photos:
        max_size = max(photo['sizes'], key=lambda x: x['width'] * x['height'])
        file_url = max_size['url']
        likes = photo['likes']['count']
        filename = f"{likes}.jpg"
        yandex_api.upload_yandex(filename, file_url, folder_name)
        count += 1
        print(f'Фото {count} успешно загружено')
        if count == 5:
            break

    yandex_api.publish(folder_name)

    vk = Vk_api(user_id=user_id, access_token=access_token)
    photos_j = vk.get_vk_photos()
    vk.save_photos_to_json('photos.json')

    # Если нужен в формате csv все фото профиля:
    # vk = Vk_api(user_id=user_id, access_token=access_token)
    # vk.save_photos_to_csv('photos.csv')
