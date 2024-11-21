from config import BOT
from telebot.types import Message, CallbackQuery, User
import keyboards
from accounts import handle_name
import requests
from datetime import datetime
from accounts import user_data

@BOT.message_handler(commands=['start'])
def start(message:Message):
    user:User = message.from_user
    print(f""" Новый пользователь!
          ID: {user.id}
          Имя: {user.first_name}
          Фамилия: {user.last_name}
          Логин: {user.username}
          Код языка: {user.language_code}
          """)
    BOT.send_message(message.chat.id, 'Hello! Please enter your name:')
    BOT.register_next_step_handler(message, handle_name )


def get_daily_horoscope(sign: str, day: str) -> dict:
    """Get daily horoscope for a zodiac sign.
    Keyword arguments:
    sign:str - Zodiac sign
    day:str - Date in format (YYYY-MM-DD) OR TODAY OR TOMORROW OR YESTERDAY
    Return:dict - JSON data
    """
    # today = datetime.today().strftime("%Y-%m-%d")
    # if day > today:
    #     return {"error": "This API does not support future dates."}
    url = "https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily"
    params = {"sign": sign, "day": day}
    response = requests.get(url, params)

    return response.json()



@BOT.message_handler(func=lambda message: message.text.lower() == 'horoscope')
def sign_handler(message):
    text = "What's your zodiac sign?\nChoose one:"
    sent_msg = BOT.send_message(message.chat.id, text, reply_markup=keyboards.get_sign_keyboard())
    BOT.register_next_step_handler(sent_msg, day_handler)



def day_handler(message):
    sign = message.text
    text = "What day do you want to know?\nChoose one: "
    sent_msg = BOT.send_message(
        message.chat.id, text, reply_markup=keyboards.get_day_keyboard())
    BOT.register_next_step_handler(sent_msg, process_day_choice, sign.capitalize())

def process_day_choice(message, sign):
    day = message.text.upper()  # Преобразуем текст в верхний регистр, чтобы избежать ошибок

    if day == 'TODAY' or day == 'TOMORROW' or day == 'YESTERDAY':
        # Если выбран один из стандартных вариантов, сразу переходим к гороскопу
        fetch_horoscope(message, sign, day)
    elif day == 'ENTER_DATE':
        # Если выбран "ENTER_DATE", запрашиваем у пользователя дату
        BOT.send_message(message.chat.id, "Please enter the date in the format YYYY-MM-DD.")
        BOT.register_next_step_handler(message, process_user_date, sign)
    elif day == 'BACK':
        # Если выбран "back", возвращаем в начальное меню
        start(message)
    else:
        # Если пользователь ввел что-то некорректное, запрашиваем снова
        BOT.send_message(message.chat.id, "Please choose a valid day from the options.")
        BOT.register_next_step_handler(message, process_day_choice, sign)

def process_user_date(message, sign):
    try:
        # Преобразуем строку в объект datetime для проверки формата
        day = datetime.strptime(message.text, "%Y-%m-%d")
                # Проверяем, больше ли введённая дата сегодняшней
        if day.date() > datetime.now().date():
            BOT.send_message(
                message.chat.id,
                "The date you entered is in the future. Unfortunately, we cannot provide a horoscope for future dates."
            )
            BOT.register_next_step_handler(message, process_user_date, sign)
            return  # Завершаем выполнение текущей функции
        fetch_horoscope(message, sign, day.strftime("%Y-%m-%d"))  # Передаем дату в правильном формате
    except Exception as e:
        # Если дата введена неверно
        BOT.send_message(message.chat.id, "Invalid date format. Please use YYYY-MM-DD.")
        BOT.register_next_step_handler(message, process_user_date, sign)

    

def fetch_horoscope(message, sign, day):
    user = user_data.get(message.chat.id, {})
    user_name = user.get('name', 'friend')  # Имя по умолчанию
    horoscope = get_daily_horoscope(sign, day)
    data = horoscope["data"]
    horoscope_message = f'*Horoscope:* {data["horoscope_data"]}\n*Sign:* {sign}\n*Day:* {data["date"]}'
    BOT.send_message(message.chat.id, f"Here's your horoscope, {user_name} !")
    BOT.send_message(message.chat.id, horoscope_message, parse_mode="Markdown")
        # Отправляем клавиатуру с возможностью выбрать новый день
    text = "You can choose another day or get back :"
    sent_msg = BOT.send_message(
        message.chat.id, text, reply_markup=keyboards.get_day_keyboard())
    BOT.register_next_step_handler(sent_msg, process_day_choice, sign)



if __name__ == '__main__':
    BOT.polling(non_stop=True)