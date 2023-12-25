from aiogram.fsm.state import State, StatesGroup


class Url(StatesGroup):
    name = State()


class AdminUrl(StatesGroup):
    name = State()
    url = State()

