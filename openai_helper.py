import openai
import constants
import random
import string


def generate_random_string(length):
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for i in range(length))
    return rand_string


class OpenAI:
  def __init__(self, api_key):
    openai.api_key = constants.OPENAI_API
    self.history = []
    self.params = []
    
    
  def set_params(self, params):
    self.params = params
    
    
  def get_response(self, message):
    num = 0
    history_message = "\n".join(self.params) + '\n' + "\n".join(self.history) + "\n"
    k = 0
    while len(history_message) > 4096:
      k+=1
      self.history = self.history[1:]
      history_message = "\n".join(self.params) + '\n' + "\n".join(self.history) + "\n"

    context = history_message
    full_message = context + 'prompt: ' + message

    response = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo-0301',
        messages = [
            {'role': 'user', 'content': full_message}
        ],
        temperature=0.5,
        max_tokens=2048,
        stop=None,
        n = 5,
    )
    new_response = random.choice(response.choices)['message']['content']
    full_message += f'\ncompletion: {new_response}'

    self.history.append(full_message)
    return new_response, self.history
