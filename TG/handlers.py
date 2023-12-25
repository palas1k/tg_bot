from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from DATABASE.db import User, Reporting, WhiteList
from TG.commands import setup_bot_commands
from TG.kb import main_kb, main_kb_admin, types, dp, F, Url, FSMContext, AdminUrl
from TG.text import main_text, main_text_admin, repeat_report, repeat_waiting, no_no_no, url_is_add_text, \
    url_access_text, error_url_text, waiting_url_text
from TG.config import id_admin

router = Router()


@router.message(Command("report"))
@router.message(Command("start"))
async def start_handler(msg: Message):
    await setup_bot_commands(msg.bot)
    user = await User.get_user(msg.from_user.first_name)
    if user is None:
        last_name = msg.from_user.last_name
        await User.create(User(first_name=msg.from_user.first_name, id_tg=msg.from_user.id, ban="no",
                               last_name=last_name))
    if id_admin == msg.from_user.id:
        await msg.answer(main_text_admin, reply_markup=main_kb_admin.as_markup())
    else:
        await msg.answer(main_text, reply_markup=main_kb.as_markup())


@router.message(AdminUrl.url)
async def add_white_list(message: Message, state: FSMContext):
    if message.text.find("https://") != 0 and message.text.find("http://") != 0:
        await message.answer(error_url_text)
        return
    domen = message.text.lower().split("/")[2]
    await state.update_data(url=domen)
    get_state = await state.get_data()
    whitelist = await WhiteList.get_list(domen)
    if whitelist:
        await message.answer(url_is_add_text)
        return
    await WhiteList.create(WhiteList(get_state["name"], domen))
    await message.answer(url_access_text)


@router.message(Url.name)
async def get_url_user(message: Message, state: FSMContext):
    await state.update_data(name=message.text.lower())
    reporting = await Reporting.get_report(message.text.lower())
    if reporting:
        if reporting.state == "Waiting":
            await message.answer(waiting_url_text)
            return
        await message.answer(repeat_report)
        return
    domen = message.text.lower().split("/")[2]
    white_list = await WhiteList.get_list(domen)
    if white_list:
        await message.answer(no_no_no.format(white_list.name))
        return
    white_list = await WhiteList.get_list(message.text.lower())
    if white_list:
        await message.answer(no_no_no.format(white_list.name))
        return
    user = await User.get_user(message.from_user.first_name)
    await Reporting.create(Reporting(url=message.text.lower(), user_id=user.id, state="Waiting"))

    await message.answer(repeat_waiting)
