import requests
import telebot
from telebot import types
import config
import time

bot = telebot.TeleBot(config.TOKEN)

codes = "lolz"

@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.id in config.admin_list:
        markup = types.InlineKeyboardMarkup()

        markup.add(types.InlineKeyboardButton(text="Поменять код", callback_data="change_code"))
        markup.add(types.InlineKeyboardButton(text="Парсить", callback_data="pars"))

        bot.send_message(message.from_user.id, text="Здравия Желаю! Вот ваше меню админа: ", reply_markup=markup)

    else:

        code = bot.send_message(message.from_user.id, text="Введите кодовое слово: ")
        
        bot.register_next_step_handler(code, get_code)
    

@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    if call.data == "change_code":
        ccc = bot.send_message(call.from_user.id, text="Введите кодовое слово:")

        bot.register_next_step_handler(ccc, ch_co)

    if call.data == "pars":
        with open(f'isch1.png', 'rb') as photo:
            short = bot.send_photo(call.from_user.id, photo, caption="Здравия Желаю! Для парсинга постов введите краткое название сообщества:")

        bot.register_next_step_handler(short, owner)

def get_code(message):
    if message.text == codes:
        with open(f'isch1.png', 'rb') as photo:
            short = bot.send_photo(message.from_user.id, photo, caption="Здравия Желаю! Для парсинга постов введите краткое название сообщества:")

        bot.register_next_step_handler(short, owner)

    else:
        bot.send_message(message.from_user.id, text="Неправильный код")

def ch_co(message):
    global codes

    codes = message.text

    bot.send_message(message.from_user.id, text=f"Код установлен ({codes})")

    markup = types.InlineKeyboardMarkup()

    markup.add(types.InlineKeyboardButton(text="Поменять код", callback_data="change_code"))
    markup.add(types.InlineKeyboardButton(text="Парсить", callback_data="pars"))

    bot.send_message(message.from_user.id, text="Здравия Желаю! Вот ваше меню админа: ", reply_markup=markup)

def owner(message):
    global urls
    urls = message.text

    with open(f'isch2.png', 'rb') as photo:
        own = bot.send_photo(message.from_user.id, photo, caption="Введите id сообщества со знаком - :")

    bot.register_next_step_handler(own, quer)

def quer(message):
    global owne
    owne = message.text

    q = bot.send_message(message.from_user.id, text="Введите ключевыую фразу или слово, если их несколько, что вводите через | :")
    
    bot.register_next_step_handler(q, para)

def para(message):
    qu = message.text

    url = "https://api.vk.com/method/wall.search"

    try:
        params = {
            "access_token": config.VK_TOKEN,
            "owner_id": int(owne),
            "v": "5.154",
            "query": qu,
        }
        response = requests.get(url, params=params)
        data = response.json()
        items = data["response"]["items"]

        for item in items:
            text_post = item.get("text").strip() #Получаем текст поста
            url_sec = str(item['from_id']) + '_' + str(item['id'])
            url = f"https://vk.com/{urls}?w=wall{url_sec}"
            bot.send_message(message.from_user.id, text=f"{url}\n {text_post}")

    except:
        bot.send_message(message.from_user.id, text="Данные были введены не верно")

        if message.from_user.id == 5089804935:
            markup = types.InlineKeyboardMarkup()

            markup.add(types.InlineKeyboardButton(text="Поменять код", callback_data="change_code"))
            markup.add(types.InlineKeyboardButton(text="Парсить", callback_data="pars"))

            bot.send_message(message.from_user.id, text="Здравия Желаю! Вот ваше меню админа: ", reply_markup=markup)

        else:
            with open(f'isch1.png', 'rb') as photo:
                short = bot.send_photo(message.from_user.id, photo, caption="Здравия Желаю! Для парсинга постов введите краткое название сообщества:")

            bot.register_next_step_handler(short, owner)


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            time.sleep(3)
            print(e)