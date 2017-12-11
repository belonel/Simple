import telebot

token = '479114083:AAFrgSo0dmotOjpEvZVcHcrV423tVUm4Id0'
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start', 'test'])
def main(message):
    bot.send_message(message.chat.id, 'Привет!Простой бот работает')

if __name__ == '__main__':
     bot.polling(none_stop=True)
