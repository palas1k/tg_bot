from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types, Dispatcher, F

from TG.text import (report_inline, admin_inline, report_text_url, add_site_white_list, add_site_social_network,
                     variable_admin, input_url_text)
from TG.states import Url, AdminUrl

dp = Dispatcher(storage=MemoryStorage())

main_kb = InlineKeyboardBuilder()
main_kb.button(text=f"{report_inline}", callback_data=f"{report_inline}")
main_kb_admin = InlineKeyboardBuilder()
main_kb_admin.button(text=f"{admin_inline}", callback_data=f"{admin_inline}")
main_kb_admin.button(text=f"{report_inline}", callback_data=f"{report_inline}")

add_inline_site = InlineKeyboardBuilder()
add_inline_site.button(text=add_site_white_list, callback_data=add_site_white_list)
add_inline_site.button(text=add_site_social_network, callback_data=add_site_social_network)


@dp.callback_query(F.data == report_inline)
async def report_send(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id,
                                                               message_id=callback_query.message.message_id,
                                                               inline_message_id=callback_query.inline_message_id,
                                                               reply_markup=None)
    await callback_query.message.answer(report_text_url)
    await state.set_state(Url.name)


@dp.callback_query(F.data == admin_inline)
async def two_variable(callback_query: types.CallbackQuery):
    await callback_query.message.answer(variable_admin, reply_markup=add_inline_site.as_markup())


@dp.callback_query(F.data == add_site_social_network)
@dp.callback_query(F.data == add_site_white_list)
async def add_site(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id,
                                                               message_id=callback_query.message.message_id,
                                                               inline_message_id=callback_query.inline_message_id,
                                                               reply_markup=None)
    if callback_query.data.lower() == add_site_social_network.lower():
        await state.update_data(name=add_site_social_network.lower())
    else:
        await state.update_data(name=add_site_white_list.lower())
    await callback_query.message.answer(input_url_text)
    await state.set_state(AdminUrl.url)
