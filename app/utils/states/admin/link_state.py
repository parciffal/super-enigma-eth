from aiogram.fsm.state import StatesGroup, State


class LinkState(StatesGroup):
    link = State()
    name = State()
