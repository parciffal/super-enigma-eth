from aiogram.filters.callback_data import CallbackData

from enum import Enum


class AdsActions(str, Enum):
    ADD = "add"
    DELETE = "delete"
    EDIT_SHOW = "show"
    EDIT_NAME = "name"
    EDIT_CHAIN = "chain"
    VIEW = "view"
    SET_CHAIN = "set_chain"
    CHANGE_CHAIN = "edit_chain"
    DELETE_ADS = "delete_ads"
    SHOW_ADS = "show_ads"
    BACK = "back"


class AdsCB(CallbackData, prefix="admin_ads"):
    action: str
    ads_id: int
