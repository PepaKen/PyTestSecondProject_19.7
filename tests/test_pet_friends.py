from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Проверка того, что статус отправляемого запроса 200 и в результате есть слово key"""
    status, result = pf.get_api_key(email, password)

    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """Проверка того, что мы получаем не пустой список питомцев (filter = ' ' or 'my_pets')"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result["pets"]) > 0


def test_add_new_pet_with_valid_data(name='Сыченец', animal_type='сыч',
                                     age='16', pet_photo='images/owl.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца среди своих питомцев"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")


def test_successful_add_new_pet_without_photo(name="Неважно", animal_type="Жив", age='3'):
    """Проверяем что можно добавить питомца без фото"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name


def test_successful_add_photo_of_my_pet(pet_photo='images/owl.jpg'):
    """Проверяем что можно добавить фотографию питомцу"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        assert status == 200
    else:
        raise Exception('Cant find a pet')


def test_get_api_key_for_invalid_user(email=invalid_email, password=invalid_password):
    """Проверка того, что статус отправляемого запроса 403"""
    status, result = pf.get_api_key(email, password)

    assert status == 200
    assert 'key' in result


def test_get_list_of_pets_by_incorrect_filter(filter='incorrect'):
    """Проверка того, что мы не получим список питомцев по некорректному фильтру"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result["pets"]) > 0


def test_successful_delete_pet_in_all_pets():
    """Проверяем возможность удаления не своего питомца"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, all_pets = pf.get_list_of_pets(auth_key)
    pet_id = all_pets['pets'][0]['id']
    if len(all_pets['pets']) > 0:
        status, _ = pf.delete_pet(auth_key, pet_id)
        _, all_pets = pf.get_list_of_pets(auth_key)
    else:
        raise Exception('Cant find a pet')

    assert status == 200
    assert pet_id not in all_pets.values()






