from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('horoscope'), 
                 KeyboardButton('Send Contact', request_contact=True),
                 KeyboardButton('Send Geolocation', request_location=True)
                 )
    return keyboard


def get_sign_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    zodiac_signs = [
        'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra',
        'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
    ]
    for sign in zodiac_signs:
        keyboard.add(KeyboardButton(sign))
    return keyboard

def get_day_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    days = ['TODAY', 'TOMORROW', 'YESTERDAY', 'ENTER_DATE', 'BACK']
    for day in days:
        keyboard.add(KeyboardButton(day))
    return keyboard




# def get_inline_keyboard():
#     keyboard = InlineKeyboardMarkup(row_width=3)  # Adjust row_width as needed
#     zodiac_signs = [
#         'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra',
#         'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
#     ]
#     for sign in zodiac_signs:
#         keyboard.add(InlineKeyboardButton(sign, callback_data=sign))
#     return keyboard

# def get_day_inline_keyboard():
#     keyboard = InlineKeyboardMarkup(row_width=2)  # Adjust row_width if needed
#     days = ['TODAY', 'TOMORROW', 'YESTERDAY']
    
#     # Adding buttons for predefined options
#     for day in days:
#         keyboard.add(InlineKeyboardButton(day, callback_data=day))
    
#     # Adding an option for a custom date input
#     keyboard.add(InlineKeyboardButton('Enter a specific date (YYYY-MM-DD)', callback_data='custom_date'))
    
#     return keyboard