from aiogram.filters.callback_data import CallbackData

from enum import Enum


#
class AdminMenuActions(str, Enum):
    GROUPS = "👥 Goups"
    ADMINS = "👮 Admins"
    ADS = "📰 Ads"
    BACK = "back"
    CLOSE = "❌ Close"
    ADD_ADS = "add_ads"


#
class AdminMenuCB(CallbackData, prefix="admin_menu"):
    action: str
