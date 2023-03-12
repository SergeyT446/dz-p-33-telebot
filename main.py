# Создать чат бота который играет с пользователем в города.
# Бот следит что бы пользователь не повторял города которые 
# уже были и города которые не подходят на ответ.

from dotenv import load_dotenv
import random
import telebot
import os

load_dotenv()
bot = telebot.TeleBot(os.getenv('TOKEN'))


def get_random_city():
    with open('cities_names.txt', encoding='utf-8') as f:
        cities = f.read().splitlines()
    return random.choice(cities)

def get_random_city_by_last_letter(previous_cities, last_letter):
    with open('cities_names.txt', encoding='utf-8') as f:
        cities = f.read().splitlines()

    matching_cities = [city for city in cities if
                       city[0].lower() == last_letter.lower() and
                       city not in previous_cities]

    if not matching_cities:
        return None
    return random.choice(matching_cities)

def is_city_in_file(city):
    with open('cities_names.txt', encoding='utf-8') as f:
        cities = f.read().splitlines()
    return city in cities

previous_cities = []

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,"Добро пожаловать в игру 'Города'! Введите название города, чтобы начать.")
    bot.send_message(message.chat.id,"Чтобы закончить игру введите : end ")
@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text.lower() == "end":
        bot.send_message(message.chat.id, "Игра остановлена.")
        previous_cities.clear()
        return
    if not message.text.isalpha():
        bot.send_message(message.chat.id, "Некорректный ввод. Пожалуйста, введите только буквы.")
        return
    if not is_city_in_file(message.text):
        bot.send_message(message.chat.id, "Такого города нет в списке. Попробуйте еще раз.")
        return
    if message.text in previous_cities:
        bot.send_message(message.chat.id, "Этот город уже был назван. Попробуйте другой.")
        return
    previous_cities.append(message.text)
   
    if message.text[-1].lower() in ['ь', 'ы', 'й']:
        last_letter = message.text[-2]
        random_city = get_random_city_by_last_letter(previous_cities, last_letter)
    else:    
        last_letter = message.text[-1]
        random_city = get_random_city_by_last_letter(previous_cities, last_letter)
    bot.send_message(message.chat.id, "Мой город - " + random_city)
    previous_cities.append(random_city)
    if previous_cities[-1][-1] in ['ь', 'ы', 'й']:
        bot.send_message(message.chat.id, "Вам на предпоследнюю")



bot.polling()
   




