import logging
from aiogram import types

from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton

import db as database
from button.buttons_menu import buttons, user_buttons, help_button, help

from bot import bot, dp


# CHECK ADMIN
class MyFilter(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin):
        self.is_admin = is_admin

    async def check(self, message: types.Message):
        user = await bot.get_chat_member(message.chat.id, message.from_user.id)
        return user.is_chat_admin()


dp.filters_factory.bind(MyFilter)


async def start_on(_):
    print('онлайн')
    database.sql_connect()


# ADMINS
@dp.message_handler(commands=['start', 'начать'], is_admin=True)
async def com_start(message: types.Message):
    await database.db_load(message)


@dp.edited_message_handler(commands=['посмотреть', 'профили'])
@dp.message_handler(commands=['посмотреть', 'профили'])
async def mes_send(message: types.Message):
    await database.db_load(message)


@dp.edited_message_handler(commands=['помощь', 'help'])
@dp.message_handler(commands=['помощь', 'help'])
async def send_help(message: types.Message):
    await message.answer(
        f'Перечень доступных команд.\nДля просмотра всех профилей /профили \n Для загрузки своего профиля /загрузить',
        reply_markup=help_button)


# ADMIN
class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    text = State()


async def check_adm(message: types.Message):
    await bot.send_message(message.from_user.id, 'Выберите команду Админ', reply_markup=buttons)


async def activ_fsm(message: types.Message):
    await FSMAdmin.photo.set()
    await message.reply('фото', reply_markup=ReplyKeyboardRemove())
    await message.answer('Если вы передумали -> /отмена')


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.reply('имя')


async def name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
        await FSMAdmin.next()
        await message.reply('Текст')


async def text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text

    await database.db_import(state)
    await message.reply('Вы успешно загрузили профиль')
    await state.finish()


async def cancel(messages: types.Message, state: FSMContext):
    fsm_state = await state.get_state()
    if not fsm_state:
        return
    await state.finish()
    await messages.reply('Начните заного', reply_markup=user_buttons)


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(check_adm, commands=['admin'], is_admin=True)
    dp.register_message_handler(activ_fsm, commands=['загрузить', 'start', 'начать'], state=None)
    dp.register_message_handler(cancel, state="*", commands='отмена')
    dp.register_message_handler(cancel, Text(equals='отмена', ignore_case=True), state='*')
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(name, content_types=['text'], state=FSMAdmin.name)
    dp.register_message_handler(text, content_types=['text'], state=FSMAdmin.text)


register_handlers_admin(dp)


# DELETE
@dp.callback_query_handler(lambda x: x.data)
async def delete_delete_profile(callback: types.CallbackQuery):
    num = int(callback.data)
    await database.db_delete(num)
    await callback.answer(text=f'Запись под ID {num} удалена', show_alert=True)



@dp.message_handler(commands=['удалить'])
async def message_delete(message: types.Message):
    id = await database.load_delete()
    print(id)
    for i in id:
        print(i, i[0])
        await message.answer(f'Профиль{i[0]}', reply_markup=InlineKeyboardMarkup()
                             .add(InlineKeyboardButton(f'Удалить{i[0]}', callback_data=f'{i[0]}')))


# USERS
@dp.message_handler()
async def other_messages(message: types.Message):
    await message.answer('Для просмотра доступных команд /help', reply_markup=help)


executor.start_polling(dp, skip_updates=True, on_startup=start_on)
logging.basicConfig(level=logging.INFO)
