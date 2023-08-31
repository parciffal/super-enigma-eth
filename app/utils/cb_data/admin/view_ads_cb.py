from aiogram.filters.callback_data import CallbackData
from enum import StrEnum


class ViewAdsActions(StrEnum):
    EDIT = "edit_ads"
    BACK = "back_ads"
    CHG_NAME = "chg_name"
    CHG_DESC = "chg_desc"
    CHG_DELAY = "chg_delay"
    CHG_SHOW = "chg_show"
    CHG_MEDIA = "chg_media"
    CHG_SHOW_IN_COM = "chg_show_com"
    BACK_TO_ADD = "back_to_ads"
    CONTINUE = "continue"


class ViewAdsCB(CallbackData, prefix="view_ads"):
    ads_id: int
    action: str
