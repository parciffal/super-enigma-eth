from aiogram.fsm.state import State, StatesGroup


class EditAdsState(StatesGroup):
    add_ads = State()
    ads_name = State()
    ads_description = State()
    ads_media = State()
    ads_left_time = State()
