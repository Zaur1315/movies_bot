# Скрипт для получения данных с Апи.
import requests
import json
from config import KINOPOISK_API  # Импортируем код апи из файла config.py.
# Добавляем привязку к дате (Нужно для отбражение Топов).
from datetime import date

# Headers
headers = {
    'X-API-KEY': KINOPOISK_API,
    'Content-Type': 'application/json'
}

# Ключивые слова для получения Топов.
month_select = ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE',
                'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER']


# Переменные для параметров функции
dateMonth = month_select[date.today().month - 1]
dateYear = date.today().year


# Функция получения Топ фильмов. по умолчанию выдает 36 последних примьер. Получаем данные через request и передаем в переменную response список json. Далее получаемые данные приобразуем к словарю с нужными нам ключами.
def rated_films(year=dateYear, month=dateMonth):
    try:
        global headers
        info = requests.get(
            f'https://kinopoiskapiunofficial.tech/api/v2.2/films/premieres?year={year}&month={month}', headers=headers)
        respose = json.loads(info.content)
        item_list = respose['items']
        let = dict()
        for i in item_list:
            genres = []
            countries = []
            for k in i['genres']:
                for y in k:
                    genres.append(k[y])
            for k in i['countries']:
                for y in k:
                    countries.append(k[y])
            let[i['kinopoiskId']] = {
                'nameRu': f"{ i['nameRu'] if 'nameRu' in i else i['nameEn']}",
                'nameEn': f"{ i['nameEn'] if 'nameEn' in i and len(i['nameEn'])>0 else i['nameRu']}",
                'year': f"{i['year'] if 'year' in i else ''}",
                'posterUrlPreview': f"{i['posterUrlPreview'] if 'posterUrlPreview' in i else ''}",
                'countries': countries,
                'genres': genres
            }
    except:
        let = 'Что то пошло не так.'
    finally:
        return let


# Функция поиска фильмов. Получаем данные через request и передаем в переменную response список json. Далее получаемые данные приобразуем к словарю с нужными нам ключами.
def search_films_by_keyword(word):
    try:
        let = dict()
        global headers

        info = requests.get(
            f'https://kinopoiskapiunofficial.tech/api/v2.1/films/search-by-keyword?keyword={word}', headers=headers)
        respose = json.loads(info.content)
        item_list = respose['films']
        for i in item_list:
            genres = []
            countries = []
            for k in i['genres']:
                for y in k:
                    genres.append(k[y])
            for k in i['countries']:
                for y in k:
                    countries.append(k[y])

            let[i['filmId']] = {
                'nameRu': f"{ i['nameRu'] if 'nameRu' in i else i['nameEn']}",
                'nameEn': f"{ i['nameEn'] if 'nameEn' in i else i['nameRu']}",
                'year': f"{i['year'] if 'year' in i else ''}",
                'description': f"{ i['description'] if 'description' in i else ''}",
                'rating': f"{i['rating'] if 'rating' in i else ''}",
                'posterUrlPreview': f"{i['posterUrlPreview'] if 'posterUrlPreview' in i else ''}",
                'countries': countries,
                'genres': genres
            }
    except:
        let = 'Что-то пошло не так. Проверьте соединение.'
    finally:
        return let


'''

Та же функция но с поиском по по имени.
Закоментировано потому, у многих фильмов отсутсвуют названия оригинала и рейтинг. При желании можно настроить этот поиск в замену дугому.


def search_films_by_keyword(word):
    let = dict()
    global headers
    info = requests.get(
        f'https://kinopoiskapiunofficial.tech/api/v2.2/films?order=RATING&type=ALL&ratingFrom=0&ratingTo=10&yearFrom=1000&yearTo=3000&keyword={word}', headers=headers)
    respose = json.loads(info.content)
    item_list = respose['items']
    for i in item_list:
        genres = []
        countries = []
        for k in i['genres']:
            for y in k:
                genres.append(k[y])
        for k in i['countries']:
            for y in k:
                countries.append(k[y])

        let[i['kinopoiskId']] = {
            'nameRu': f"{ i['nameRu'] if 'nameRu' in i else i['nameEn']}",
            'nameEn': f"{ i['nameEn'] if 'nameEn' in i else i['nameRu']}",
            'year': f"{i['year'] if 'year' in i else ''}",
            'description': f"{ i['description'] if 'description' in i else ''}",
            'rating': f"{i['rating'] if 'rating' in i else ''}",
            'posterUrlPreview': f"{i['posterUrlPreview'] if 'posterUrlPreview' in i else ''}",
            'countries': countries,
            'genres': genres
        }

    return let



'''
