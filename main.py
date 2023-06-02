import telebot
import constants
import openai
import openai_helper
import time
import threading
import datetime

bot = telebot.TeleBot(constants.TELEGRAM_BOT_API)
users = {}
select_params = False


class StoppableThread():
    def __init__(self,  bot, chat_id):
        self.stop_flag = threading.Event()
        threading.Thread(target=self.typing_func, args=(bot, chat_id,)).start()
        self.bot = bot
        self.chat_id = chat_id
        
        
    def stop(self):
        self.stop_flag.set()
        
        
    def typing_func(self, bot, chat_id):
      while not self.stop_flag.is_set():
        bot.send_chat_action(chat_id, 'typing')
        time.sleep(3)

        
@bot.message_handler()
def url(message):
    global select_params
    user_id = str(message.from_user.id)
    if not user_id in users:
      users[user_id] = openai_helper.OpenAI(constants.OPENAI_API)
      users[user_id].get_response('Не нужно дополнять мои фразы, пока я не попрошу.\n')

    if message.text == "/start":
      bot.send_message(message.from_user.id, constants.GREETINGS)
    elif "/params" == message.text or select_params:
      if not select_params:
        bot.send_message(message.from_user.id, "Запиши параметры через Shift+Enter")
      else:
        bot.send_message(message.from_user.id, "Принято")
        try:
          params_arr = ' '.join(message.text.split()).split('.\n')
          users[user_id].set_params(['Не нужно дополнять мои фразы, пока я не попрошу.\n'] + params_arr)
          print(params_arr)
        except:
          bot.send_message(message.from_user.id, "Введи нормально")

      select_params = not select_params

    elif "/new" == message.text:
      users[user_id] = openai_helper.OpenAI(constants.OPENAI_API)
      bot.send_message(message.from_user.id, 'Новая сессия создана')
    else:
      thr = StoppableThread(bot, message.from_user.id)

      response, history = users[user_id].get_response(message.text + ".")

      bot.send_message(message.from_user.id, response)

      thr.stop()

bot.polling(none_stop=True, interval=0)
