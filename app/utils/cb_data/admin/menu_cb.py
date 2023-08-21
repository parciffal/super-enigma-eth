from aiogram.filters.callback_data import CallbackData

from enum import StrEnum


class AdminMenuActions(StrEnum):
    GROUPS = "👥 Goups"
    ADMINS = "👮 Admins"
    ADS = "📰 Ads"


class AdminMenuCB(CallbackData, prefix="admin_menu"):
    action: AdminMenuActions
