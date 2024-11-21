from telebot.types import Message 
from config import BOT
import keyboards

user_data = {}

def handle_name(message:Message):
    from main import sign_handler
    name = message.text
    if name:
        user_data[message.chat.id] = {'name': name}
        BOT.send_message(message.chat.id, f'Nice to meet you, {name} :) What would you like to do?', reply_markup=keyboards.get_main_keyboard())
        BOT.register_next_step_handler(message, sign_handler)
    else:
        BOT.send_message(message.chat.id, 'Error! Please enter your name:')
        BOT.register_next_step_handler(message, handle_name)
