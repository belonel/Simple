import telebot
import json
import config

token = config.token
bot = telebot.TeleBot(token)
tag = ''
phrase = ''

@bot.message_handler(commands=['start', 'find'])
def main(message):
    sent = bot.send_message(message.chat.id, 'Привет!Введи слово и я выдам тебе цитату.')
    bot.register_next_step_handler(sent, fileSearch)

@bot.message_handler(commands=['adminbot'])
def adminbot(message):
    sent = bot.send_message(message.chat.id, "Вы перешли в версию для администрирования.\n"
                                             "Выберите действие:\n"
                                             "1 - Добавить новую цитату\n"
                                             "2 - Удалить последнюю\n"
                                             "3 - Выйти из меню администрирования")
    bot.register_next_step_handler(sent, admin)


def check (message):
    if message.text == '/start' or message.text == '/adminbot' or message.text == '/find':
        return 1
    else:
        return 0


def addPhrase(message):
    with open('DB.json', encoding='utf-8') as data_file:
        data = json.loads(data_file.read())

    id = str(len(data) + 1)

    element = {
        "ID": id,
        # "Tag": tag,
        # "Phrase": phrase
        "Тэг": tag,
        "Цитата": phrase
    }

    try:
        data.append(element)
        with open('DB.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
    except:
        bot.send_message(message.chat.id, "ooops")
    sent = bot.send_message(message.chat.id, "№ {i}\nТэги: {t}\nЦитата: {p}\nЗаписаны в базу данных".format(i = id, t = tag, p = phrase))
    bot.register_next_step_handler(sent, admin)
    bot.send_message(message.chat.id, "Выберите одну из команд\n"
                                      "1 - Добавить новую цитату\n"
                                      "2 - Удалить последнюю\n"
                                      "3 - Выйти из меню администрирования")


def deleteLastPhrase(message):
    with open('DB.json', encoding='utf-8') as data_file:
        data = json.loads(data_file.read())

    try:
        data.pop()
        with open('DB.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
    except:
        bot.send_message(message.chat.id, "ooops")

    id = len(data) - 1
    sent = bot.send_message(message.chat.id,
                            "Теперь последняя цитата:\n№{i}\nТэг: {t}\nЦитата: {p}".format(i=id+1, t=data[id]["Цитата"], p=data[id]["Цитата"]))
    bot.register_next_step_handler(sent, admin)

    bot.send_message(message.chat.id, "Выберите одну из команд\n"
                                      "1 - Добавить новую цитату\n"
                                      "2 - Удалить последнюю\n"
                                      "3 - Выйти из меню администрирования")

def find(message):
    # Открываем файл базы данных для чтения
    # Пробегать циклом по базе данных и искать цитату по введенному слову (message.text)
    # Вывести цитату
    # Проверить message.text , если ввели /adminbot , вызвать admin
    # Рекурсивно вызвать find(message)
    bot.send_message(message.chat.id, "Выполняется поиск...")

def fileSearch(message):
    if (check(message) == 0):
        with open('DB.json', encoding='utf-8') as data_file:
            data = json.loads(data_file.read())

        for i in range(0, len(data)):
            element = data[i]["Тэг"]
            for element in data[i]["Тэг"]:
                if message.text == element:
                    sent = bot.reply_to(message, data[i]["Цитата"])
                    bot.register_next_step_handler(sent, fileSearch)
                    return
        else:
            str = bot.send_message(message.chat.id, 'Цитаты по такому слову не найдено, попробуй что-нибудь еще')
            bot.register_next_step_handler(str, fileSearch)
    else:
        return


def inputTag(message):
    if (check(message) == 1):
        return
    global tag
    tag = message.text.split(', ')
    sent = bot.send_message(message.chat.id, "Теперь введите цитату без ковычек")
    bot.register_next_step_handler(sent, inputPhrase)


def inputPhrase(message):
    if (check(message) == 1):
        return
    global phrase
    phrase = message.text
    addPhrase(message)

def admin(message):
    if (check(message) == 1):
        return
    if message.text == '1':
        sent = bot.send_message(message.chat.id, "Введите тэги.\nФормат: \"первый, второй, третий\".\nПодряд с маленькой буквы разделяя запятой")
        bot.register_next_step_handler(sent, inputTag)
    elif message.text == '2':
        deleteLastPhrase(message)
    elif message.text == '3':
        main(message)
    else:
        sent = bot.send_message(message.chat.id, "Такой функции не существует")
        bot.register_next_step_handler(sent, admin)


if __name__ == '__main__':
     bot.polling(none_stop=True)