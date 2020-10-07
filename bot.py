import config
import telebot
from ikea_availability_api import IkeaAvailability

bot = telebot.TeleBot(config.token)


@bot.message_handler(content_types=["text"])
def repeat_all(message):
    # TODO sanitize text message.
    api_service = IkeaAvailability()
    availability_response = api_service.get_availability_info(message.text)
    bot.send_message(message.chat.id, str(availability_response))


if __name__ == '__main__':
    bot.infinity_polling()
