from aiogram.fsm.state import StatesGroup, State


class GroupState(StatesGroup):
    link = State()
    name = State()
    chain = State()
