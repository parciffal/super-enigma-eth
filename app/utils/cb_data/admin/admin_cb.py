from aiogram.filters.callback_data import CallbackData

from enum import Enum


class AdminActions(str, Enum):
    ADD = "add"
    DELETE = "delete"
    EDIT_ACTIVE = "active"
    VIEW = "view"


class AdminCB(CallbackData, prefix="admin_admin"):
    action: str
    admin_id: int
