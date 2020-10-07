import config
import telebot
from ikea_availability_api import IkeaAvailability

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=["forecast"])
def forecast(message):
    # TODO find better way to get parameter.
    # TODO sanitize text message.
    product_id = message.text[len("/forecast") + 1:]
    if len(product_id) == 0:
        bot.send_message(message.chat.id, 'Looks like you forgot a product ID.')
        return
    if len(product_id) != 8 or not product_id.isdigit():
        bot.send_message(message.chat.id, 'Please, type only a product ID.')
        return

    api_service = IkeaAvailability(product_id)
    forecast = api_service.availability_forecast()
    # TODO Form pretty answer.
    bot.send_message(message.chat.id, str(forecast))


@bot.message_handler(content_types=["text"])
def repeat_all(message):
    # TODO sanitize text message.
    product_id = message.text

    if len(product_id) != 8 or not product_id.isdigit():
        bot.send_message(message.chat.id, 'Please, type only a product ID.')
        return
    api_service = IkeaAvailability(product_id)
    if api_service.is_product_available():
        bot.send_message(message.chat.id, 'Happy to say the product is available at the stock!')
    else:
        bot.send_message(message.chat.id,
                         f'Unfortunately the product is out of stock!\nTry to check a forecast for {product_id}')


if __name__ == '__main__':
    bot.infinity_polling()
