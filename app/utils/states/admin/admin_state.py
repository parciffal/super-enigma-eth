from aiogram.fsm.state import StatesGroup, State


class ChangeNameState(StatesGroup):
    new_name = State()


class AdminState(StatesGroup):
    link = State()
