import os

country_dir = 'static/'
countries = os.listdir(country_dir)
countries.sort()


def create_country_list():
    country_list = []
    for country in countries:
        if not country.startswith('.'):
            if not country.startswith('style'):
                country_list.append(country)
    with open(country_dir + 'style_ru_info.txt', encoding="utf-8") as info:
        read_data = info.read().split('|')
    read_data.sort()
    country_list.sort()
    country_dict = dict(zip(country_list, read_data))

    return country_dict


def translate_countries(lang):
    country_names = create_country_list().keys()
    ru_names = create_country_list().values()
    my_dict_en = dict(zip(country_names, country_names))
    my_dict_en = {'head_countries': 'Countries where we took some pics', 'countries': my_dict_en}
    my_dict_ru = dict(zip(country_names, ru_names))
    my_dict_ru = {'head_countries': 'Страны, в которых мы сделали пару фотографий', 'countries': my_dict_ru}

    country_dict = {'en': my_dict_en, 'ru': my_dict_ru}

    return country_dict.get(lang)


def create_city_list(country):
    city_dir = 'static/' + country
    city_list = os.listdir(city_dir)
    cities = []
    for city in city_list:
        if not city.startswith('.'):
            if not city.startswith('ru'):
                cities.append(city)
    with open(city_dir + '/' + 'ru_names.txt', encoding="utf-8") as info:
        read_data = info.read().split('|')
    cities.sort()
    en_cities = dict(zip(cities, cities))
    city_dict = dict(zip(cities, read_data))

    return city_dict, en_cities


def translate_cities(lang, country):
    cities_ru, cities_en = create_city_list(country)
    country_name_ru = create_country_list().get(country)
    en_info = {'country_name': country,
               'little_text': "what we've visited there",
               'back_button': "Back to all places",
               'cities': cities_en}
    ru_info = {'country_name': country_name_ru,
               'little_text': "места, которые мы там посетили",
               'back_button': "Назад к списку мест",
               'cities': cities_ru}

    dict_cities = {'en': en_info, 'ru': ru_info}

    return dict_cities.get(lang)


def get_when(country, city):
    when_list = os.listdir(country_dir + country + '/' + city)
    when = []
    value = []
    for time in when_list:
        if not time.startswith('.'):
            if not time.startswith('ru'):
                when.append(time)
                value.append(time.replace('_', ' '))
    when.sort()
    with open(country_dir + country + '/' + city + '/' + 'ru_when.txt', encoding="utf-8") as info:
        read_data = info.read().split('|')

    when_dict_ru = dict(zip(when, read_data))
    when_dict_en = dict(zip(when, value))

    return when_dict_ru, when_dict_en


def translate_when(lang, country, city):
    when_dict_ru, when_dict_en = get_when(country, city)
    city_dict, cities_en = create_city_list(country)
    city_name_ru = city_dict.get(city)
    en_info = {'city_name': city,
               'little_text': "when we've been there",
               'back_button': "Back to places",
               'when': when_dict_en}
    ru_info = {'city_name': city_name_ru,
               'little_text': "когда мы там побывали",
               'back_button': "Назад",
               'when': when_dict_ru}

    dict_when = {'en': en_info, 'ru': ru_info}

    return dict_when.get(lang)


def get_content(country, city, when):
    img_list = os.listdir(country_dir + country + '/' + city + '/' + when)
    img_list.sort()
    img_names = []
    img_urls_en = []
    img_urls_ru = []
    img_description_en = []
    img_description_ru = []
    url_en = ''
    url_ru = ''
    for name in img_list:
        if name.startswith('info'):
            url_en = country_dir + country + '/' + city + '/' + when + '/' + 'info.txt'
            url_ru = country_dir + country + '/' + city + '/' + when + '/' + 'info_ru.txt'
        if name.startswith('IMG'):
            img_names.append('/' + country_dir + country + '/' + city + '/' + when + '/' + '%s' % name)

    try:
        with open(url_en, encoding="utf-8") as info:
            read_data_en = info.read().split('|')
        for data in read_data_en:
            data = data.strip()
            if data.startswith('IMG'):
                img_urls_en.append('/' + country_dir + country + '/' + city + '/' + when + '/' + '%s.jpg' % data)
            if data.startswith('-'):
                img_description_en.append(data.lstrip('-'))

        with open(url_ru, encoding="utf-8") as info:
            read_data_ru = info.read().split('|')
        for data in read_data_ru:
            data = data.strip()
            if data.startswith('IMG'):
                img_urls_ru.append('/' + country_dir + country + '/' + city + '/' + when + '/' + '%s.jpg' % data)
            if data.startswith('-'):
                img_description_ru.append(data.lstrip('-'))
    except FileNotFoundError:
        pass

    img_count = len(img_names)

    for img in img_urls_en and img_urls_ru:
        if img in img_names:
            img_names.remove(img)

    return img_description_en, img_description_ru, img_urls_en, img_urls_ru, img_names, img_count


def translate_content(lang, country, city, when):
    img_description_en, img_description_ru, img_urls_en, img_urls_ru, img_names, img_count = get_content(country, city, when)

    img_dict_en = dict(zip(img_urls_en, img_description_en))
    img_dict_ru = dict(zip(img_urls_ru, img_description_ru))
    uni_img_dict = {}
    for img in img_names:
        uni_img_dict[img] = ''

    img_dict_en.update(uni_img_dict)
    img_dict_ru.update(uni_img_dict)

    city_dict, cities_en = create_city_list(country)
    city_name_ru = city_dict.get(city)
    en_text = {'city': city,
               'alert': 'Get ready!',
               'count': 'Here you have',
               'photos': 'photos!',
               'back_button': 'Go back',
               'no_photos': 'There will be photos very soon ^_^',
               'img_pack': img_dict_en}
    ru_text = {'city': city_name_ru,
               'alert': 'Приготовься!',
               'count': 'На этой странице тебя ждет',
               'photos': 'фоточек!',
               'back_button': 'Вернуться обратно',
               'no_photos': 'Тут скоро появятся фоточки ^_^',
               'img_pack': img_dict_ru}

    img_dict = {'en': en_text, 'ru': ru_text}

    return img_dict.get(lang), img_count

