from aiogram import Dispatcher
from aiogram.types import *

from keyboards.inline.channels import show_channels
from keyboards.inline.users_btn import languages_btn
from loader import dp
from utils.misc.subs import check_sub_channel
from utils.misc.text_translator import text_trans
from database.connections import add_user


async def bot_start(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username
    await add_user(user_id, username)
    btn = await show_channels()
    check = check_sub_channel(message)
    if check:
        await message.answer(f"Assalomu aleykum")
    else:
        await message.answer("Botdan foydalanishdan avval quyidagi kanallarga obuna bo'ling",reply_markup=btn)

async def check_sub(call: CallbackQuery):
    check = await check_sub_channel(call)
    if check:
        await call.message.delete()
        await call.message.answer("Siz botdan to'liq foydalanish xuquqiga ega bo'ldingiz.\nBiror bir gap yozing.")
    else:
        await call.answer("Berilgan kanallarga obuna bo'ling",show_alert=True)


async def get_user_text_handler(message: Message):
    text = message.text
    btn = await languages_btn()
    channel_btn = await show_channels()
    check = await check_sub_channel(message)
    if check:
        await message.answer(text, reply_markup=btn)
    else:
        await message.answer("Botdan foydalanishdan avval quyidagi kanallarga obuna bo'ling", reply_markup=channel_btn)


async def select_lang_callback(call: CallbackQuery):
    await call.answer()
    lang = call.data.split(":")[-1]
    context = call.message.text
    result = await text_trans(context, lang)
    if context != result:
        btn = await languages_btn()
        await call.message.edit_text(result, reply_markup=btn)


def register_users_py(dp: Dispatcher):
    dp.register_message_handler(bot_start, commands=['start'])
    dp.register_message_handler(get_user_text_handler, content_types=['text'])

    dp.register_callback_query_handler(select_lang_callback, text_contains='lang:')
    dp.register_callback_query_handler(check_sub, text="sub_channel_done")