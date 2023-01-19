# Скрипт для Телеграм-бота.
# Нужные функции из библиотеки Аиограм.
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from config import BOT_TOKEN  # Токен бота из файла config.py.
from api import *  # Получение функций из вайла api.py.


# Создание диспатчера и подключение токена бота.
bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


# Приветственное сообщение бота при команде /start.
@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer('Вас приветствует КиноБот. Напишите ключивое слово для поиска или напишите слово ХИТ чтоб получить подборку горячих новинок этого месяца.')


# Отслеживание всех сообщений ботом.
@dp.message_handler()
async def search(message: types.Message):
    # Если сообщение ТОМ в любом регистре то вызывается функция rated_films. При желании можно передать в нее параметры года и месяца.
    if message.text.lower() == 'топ':
        x = rated_films()
        for i in x:
            await message.answer(f"<b>Название</b>: {x[i]['nameRu']}\n<b>Оригинал</b>: {x[i]['nameEn']}\n<b>Год</b>: {x[i]['year']}\n<b>Страна</b>: {(' '.join(x[i]['countries']))}\n<b>Жанр</b>: {(' '.join(x[i]['genres']))}\n {x[i]['posterUrlPreview']}", parse_mode="html")
    else:
        # Если в сообщении написано что либо другое, то бот принимает это как ключевое слово для поиска и вызывает функцию search_films_by_keyword куда в параметры передается слово для поиска. Поиск производится не только по названиям но и по описанию.
        x = search_films_by_keyword(message.text)
        if len(x) == 0:
            await message.answer(f'К сожалению по вашему запросу <b>{message.text}</b> ничего не найдено.', parse_mode='html')
        else:
            for i in x:
                await message.answer(f"<b>Название</b>: {x[i]['nameRu']}\n<b>Оригинал</b>: {x[i]['nameEn']}\n<b>Год</b>: {x[i]['year']}\n<b>Страна</b>: {(' '.join(x[i]['countries']))}\n<b>Жанр</b>: {(' '.join(x[i]['genres']))}\n<b>Рейтинг</b>: {x[i]['rating']}\n<b>Краткое описание</b>: {x[i]['description']}\n {x[i]['posterUrlPreview']}", parse_mode="html")

# Запуск бесконечного цикла работы бота.
if __name__ == '__main__':
    executor.start_polling(dp)
