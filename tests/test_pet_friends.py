from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os
import pytest

pf = PetFriends()


class TestsUpdated:
    @pytest.fixture(autouse=True)
    def get_key(self):
        self.pf = PetFriends()
        status, self.key = self.pf.get_api_key(valid_email, valid_password)
        assert status == 200
        assert 'key' in self.key

        yield

    def test_get_all_pets_with_valid_key(self, filter=''):
        """Проверяем что можно добавить питомца с корректными данными"""
        self.status, result = self.pf.get_list_of_pets(self.key, filter)

        assert self.status == 200
        assert len(result['pets']) > 0

    def test_add_new_pet_with_valid_data(self, name='Сыченец', animal_type='сыч',
                                         age='16', pet_photo='images/owl.jpg'):
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        self.status, result = self.pf.add_new_pet(self.key, name, animal_type, age, pet_photo)

        assert self.status == 200
        assert result['name'] == name

    def test_successful_delete_self_pet(self):
        """Проверяем возможность удаления питомца среди своих питомцев"""
        _, my_pets = self.pf.get_list_of_pets(self.key, 'my_pets')
        pet_id = my_pets['pets'][0]['id']
        self.status, _ = self.pf.delete_pet(self.key, pet_id)
        _, my_pets = self.pf.get_list_of_pets(self.key, 'my_pets')

        assert self.status == 200
        assert pet_id not in my_pets.values()

    def test_successful_update_self_pet_info(self, name='Мурзик', animal_type='Кот', age=5):
        """Проверяем возможность обновления информации о питомце"""
        _, my_pets = self.pf.get_list_of_pets(self.key, "my_pets")

        if len(my_pets['pets']) > 0:
            self.status, result = self.pf.update_pet_info(self.key, my_pets['pets'][0]['id'], name, animal_type, age)

            assert self.status == 200
            assert result['name'] == name
        else:
            raise Exception("There is no my pets")

    def test_successful_add_new_pet_without_photo(self, name="Неважно", animal_type="Жив", age='3'):
        """Проверяем что можно добавить питомца без фото"""
        self.status, result = self.pf.create_pet_simple(self.key, name, animal_type, age)

        assert self.status == 200
        assert result['name'] == name

    def test_successful_add_photo_of_my_pet(self, pet_photo='images/owl.jpg'):
        """Проверяем что можно добавить фотографию питомцу"""
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        _, my_pets = self.pf.get_list_of_pets(self.key, 'my_pets')
        if len(my_pets['pets']) > 0:
            self.status, result = self.pf.add_photo_of_pet(self.key, my_pets['pets'][0]['id'], pet_photo)
            assert self.status == 200
        else:
            raise Exception('Cant find a pet')

    def test_get_list_of_pets_by_incorrect_filter(self, filter='incorrect'):
        """Проверка того, что мы не получим список питомцев по некорректному фильтру"""
        self.status, result = self.pf.get_list_of_pets(self.key, filter)

        assert self.status == 500

    def test_successful_delete_pet_in_all_pets(self):
        """Проверяем возможность удаления не своего питомца"""
        _, all_pets = self.pf.get_list_of_pets(self.key)
        pet_id = all_pets['pets'][0]['id']
        if len(all_pets['pets']) > 0:
            self.status, _ = self.pf.delete_pet(self.key, pet_id)
            _, all_pets = self.pf.get_list_of_pets(self.key)
        else:
            raise Exception('Cant find a pet')

        assert self.status == 200
        assert pet_id not in all_pets.values()


def test_get_api_key_for_invalid_user(email=invalid_email, password=invalid_password):
    """Проверка того, что api key не будет получен при авторизации с некорректными данными"""
    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result





