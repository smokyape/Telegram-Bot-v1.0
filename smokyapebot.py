import telebot
from config import keys, TOKEN
from utils import ConvertionException, CryptoApeConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def start_message(message):
    bot.send_message(message.chat.id, f"Добро пожаловать, {message.chat.username} 🍌"
                                    f"\n"
                                    f"\nДля того, чтобы начать работу, введите "
                                    f"команду боту в следующем формате:"
                                    f"\n"
                                    f"\n<название валюты><в какую валюту перевести>"
                                    f"<количество переводимой валюты>"
                                    f"\n"
                                    f"\nУвидеть список всех доступных валют: /values")

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Слишком много/мало параметров, повторите ввод:')

        quote, base, amount = values
        total_base = CryptoApeConverter.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()



