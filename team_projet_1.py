import requests
from pprint import pprint
from config import ID_VK, TOKEN_VK


# Создаем класс пользователей VK
class VK:
    base_url = 'https://api.vk.com/method'

    def __init__(self, access_token, user_id, version):
        self.access_token = access_token
        self.user_id = user_id
        self.version = version
        self.params = {"access_token": self.access_token, "v": self.version}

    # Создаем метод для поиска пользователей VK по нужным параметрам и получения топ-трех фото
    def user_search(self, age_from, age_to, sex, city, family_status, count=1):
        params = {'age_from': age_from, 'age_to': age_to, 'sex': sex,
                  'city': city, 'status': family_status, 'count': count}
        response = requests.get(f'{self.base_url}/users.search', params={**self.params, **params})
        user_search_id = response.json()["response"]["items"][0]["id"]

        params_2 = {'owner_id': user_search_id, 'album_id': 'profile', "extended": 1}
        answer = requests.get(f'{self.base_url}/photos.get', params={**self.params, **params_2})
        photo_profile = answer.json()['response']['items']
        photo_list = []
        for item in photo_profile:
            photo_likes_dict = {}
            photo_likes_dict["url"] = item["orig_photo"]["url"]
            photo_likes_dict["likes"] = item["likes"]["count"]
            photo_list.append(photo_likes_dict)

        photo_list = sorted(photo_list, key=lambda x: x["likes"], reverse=True)[0:3]
        return photo_list




# запуск программы
if __name__ == '__main__':
    client_VK = VK(TOKEN_VK, ID_VK, 5.199)
    answer = client_VK.user_search(42, 43, 1, 26, 1)
    pprint(answer)
