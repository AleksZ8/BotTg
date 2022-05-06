from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

buttons = ReplyKeyboardMarkup(resize_keyboard=True)
b1 = KeyboardButton('/загрузить')
b2 = KeyboardButton('/удалить')
b3 = KeyboardButton('/посмотреть')

buttons.add(b1).row(b2, b3)


user_buttons = ReplyKeyboardMarkup(resize_keyboard=True)
b1 = KeyboardButton('/профили')
b3 = KeyboardButton('/загрузить')
b2 = KeyboardButton('/помощь')

user_buttons.row(b1, b2).add(b3)
help_button = ReplyKeyboardMarkup().row(b1, b2)
profile_button = ReplyKeyboardMarkup().row(b3, b2)
help = ReplyKeyboardMarkup().add(b2)


# delete = InlineKeyboardMarkup(row_with=1)
# delete.add(InlineKeyboardButton(text='удалить', callback_data='delete_profile'))