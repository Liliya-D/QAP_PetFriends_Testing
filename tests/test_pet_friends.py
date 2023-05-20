from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()

# Тест №1
def test_get_api_key_valid_user(email=valid_email, password=valid_password):
    '''Проверяем что код статуса запроса 200 и в переменной result содержится слово key'''

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


# Тест №2
def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что код статуса запроса 200 и список всех питомцев не пустой.
    Для этого при помощи метода get_app_key() получаем ключ, сохраняем его в переменной
    api_key, затем применяем метод get_list_of_pets() и проверяем статус ответа и то
    что список питомцев не пустой """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


# Тест №3
def test_add_new_pet_with_valid_data(name='Рыжий', animal_type='Бенгал',
                                     age='3', pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


# Тест №4
def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


# Тест №5
def test_update_pet_info(name='Васька', animal_type='Котейка', age='3'):
    '''Проверяем возможность изменения данных питомца'''
    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("Питомцы отсутствуют")


# Тест №6
def test_add_pets_with_valid_data_without_photo(name='Барбос', animal_type='Пёс', age='6'):
    '''Проверяем возможность добавления нового питомца без фото'''
    # Получаем ключ auth_key
    _, api_key = pf.get_api_key(valid_email, valid_password)
    # Добавляем питомца без фото
    status, result = pf.add_new_pet_without_photo(api_key, name, animal_type, age)
    # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
    assert status == 200
    assert result['name'] == name


# Тест №7
def test_add_new_photo_at_pet(pet_photo='images/Bengal.jpg'):
    '''Проверяем возможность добавления новой фотографии питомца'''
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    # Если список не пустой, то пробуем обновить его фото
    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        # Получаем список своих питомцев
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
        # Проверяем что статус ответа = 200 и фото питомца соответствует заданному
        assert status == 200
        assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("Питомцы отсутствуют")


# Тест №8
def test_add_pet_with_a_lot_of_words_in_variable_animal_type(name='Геракл', age='2', pet_photo='images/cat1.jpg'):
    """Проверка с негативным сценарием.
    Добавления питомца с полем "Породы", которое превышает 10 слов.
    Сообщение, если питомец будет добавлен в приложение с названием породы состоящим из более 10 слов."""

    animal_type = 'Гладкошерстный Британский Пушистый Азиатский Австралийский Мист Митист Турецкий Ван Шатландец Сноу-Шу'
    # Получаем ключ auth_key и добавляем питомца
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    # Получаем список animal_type и считаем кол-во слов в нем
    list_animal_type = result['animal_type'].split()
    word_count = len(list_animal_type)
    # Проверяем что статус ответа = 200 и кол-во слов не превышает 10
    assert status == 200
    assert word_count > 10
    print(f'\n Добавлен питомец с названием породы больше 10 слов. {word_count}')


#Тест 9
def test_add_pet_with_numbers_in_variable_animal_type(name='Рыжий', animal_type='898430', age='0', pet_photo='images/Bengal.jpg'):
    """Проверка с негативным сценарием. Добавление питомца с цифрами вместо букв в переменной animal_type.
    Сообщение, если питомец будет добавлен в приложение с цифрами вместо букв в поле "Порода"."""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Получаем ключ auth_key и добавляем питомца
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    # Проверяем что статус ответа = 200 и тип животного существует
    assert status == 200
    assert animal_type in result['animal_type']
    print(f'\n Добавлен питомец с цифрами вместо букв в поле "Порода". {animal_type}')


#Тест 10
def test_add_new_pet_with_unicode_symbols(name='関東弁五人の会社員اللغة العربية', animal_type='ภาษาไทย δθφ',
                                     age='①❸⓷¾', pet_photo='images/parrot.jpg'):
    """Проверяем, что можно при добавлении питомца поля принимают различные символы"""

    # Полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Получаем ключ auth_key и добавляем питомца
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    # Проверяем что статус ответа = 200 и имя питомца, порода, возраст соответствуют заданному
    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age
    print(f'\n Добавлен питомец со спец.символами вместо букв в поля "Имя", "Порода", "Возраст". {name}, {animal_type}, {age}')

