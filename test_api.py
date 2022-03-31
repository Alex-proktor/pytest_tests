import requests


# @pytest.fixture(scope="module")
def test_1_unit_update_pet_access_correct_data_get_correct_data():
    """
    Метод: https://petstore.swagger.io/v2/pet
    Авторизованный пользователь, отправляем корректные данные
    Ожидаем: отправленные данные
    """
    msg = 'Авторизованный пользователь, корректные данные,'
    correct_code = 200
    url = "https://petstore.swagger.io/v2/pet"
    data = {
        "id": 9223372016854959590,
        "category": {
            "id": 1,
            "name": "chow chow"
        },
        "name": "doggie",
        "photoUrls": [
            "https://petstore.swagger.io/v2/pet/9223372016854959590/img"
        ],
        "tags": [
            {
                "id": 2,
                "name": "guard dog"
            }
        ],
        "status": "available"
    }
    headers = {'api_key': 'special-key'}
    res = requests.put(url=url, json=data, headers=headers)
    code = res.status_code
    assert code == correct_code, f"{msg} код ответа получаем vs ожидали: {code} vs {correct_code}"
    assert data == res.json(), f"{msg} данные ответа: получаем vs ожидали: {res.json()} vs {data}"


def test_2_е2е_pet_positive():
    """
    Эндпойнт: pet https://petstore.swagger.io/v2/pet
    Сценарий:
        Создаем питомца
        Проверяем питомца
        Обновляем изображение
        Проверяем питомца
        Обновляем статус
        Проверяем по статусу
        Обновляем данные в магазине
        Проверяем обновление
        Удаляем питомца
        Проверяем отсутствие питомца

    """
    data = {
        "id": 9223372016854971000,
        "category": {
            "id": 1,
            "name": "chow chow"
        },
        "name": "doggie",
        "photoUrls": [
            "https://petstore.swagger.io/v2/pet/9223372016854959590/img"
        ],
        "tags": [
            {
                "id": 2,
                "name": "guard dog"
            }
        ],
        "status": "available"
    }
    url = "https://petstore.swagger.io/v2/pet"
    url_get_pet = f'{url}/{data["id"]}'
    url_uploadImage = f'{url}/{data["id"]}/uploadImage'
    url_find_by_status = f'{url}/findByStatus'
    headers = {'api_key': 'special-key'}

    msg_code = 'Код ответа получаем vs ожидали: '
    # code = res.status_code
    # assert code == correct_code, f"{msg} код ответа получаем vs ожидали: {code} vs {correct_code}"

    # Создаем питомца
    new_pet = requests.post(url=url, json=data, headers=headers)
    assert new_pet.status_code == 200, f"Создание питомца. {msg_code}{new_pet.status_code} vs 200"

    # Проверяем питомца
    pet = requests.get(url=url_get_pet, params=data, headers=headers)
    assert pet.status_code == 200, f"Создание питомца.{msg_code}{pet.status_code} vs 200"

    # Обновляем изображение
    test_file = 'dog.jpg'
    upload_img = requests.post(url=url_uploadImage, files={'file': test_file}, headers=headers)
    assert upload_img.status_code == 200, f"Обновление изображения. {msg_code}{upload_img.status_code} vs 200"
    # print(f'Обновляем изображение: {res} {res.text = }')

    # Обновляем данные в магазине ('status' = 'sold')
    status = 'sold'
    upload_status = {'name': data['name'], 'status': status}
    data['status'] = status
    req_upload_status = requests.post(url=url_get_pet, data=upload_status, headers=headers)
    assert req_upload_status.status_code == 200, f"Обновление статуса.{msg_code}{req_upload_status.status_code} vs 200"

    # Проверяем обновление статуса
    pet_after_status_update = requests.get(url=url_get_pet, params=data, headers=headers)
    assert pet_after_status_update.json() == data, f"Обновление статуса магазином"

    find_by_status = requests.get(url=url_find_by_status, params={'status': status}, headers=headers)
    pets = find_by_status.json()
    assert [x for x in pets if x['id'] == data['id']], f"Поиск по статусу не нашел питомца с {data['id'] = }"

    # Удаляем питомца
    del_pet = requests.delete(url=url_get_pet, headers=headers)
    assert del_pet.status_code == 200, f"Удаление питомца.{msg_code}{pet.status_code} vs 200"

    # Проверяем отсутствие питомца
    pet_after_del = requests.get(url=url_get_pet, params={'id': data['id']}, headers=headers)
    assert pet_after_del.status_code == 404, f"Питомец удален.{msg_code}{pet.status_code} vs 404"
