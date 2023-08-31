from aiogram.filters.callback_data import CallbackData

from enum import Enum


class GroupActions(str, Enum):
    ADD = "add"
    DELETE = "delete"
    EDIT_SHOW = "show"
    EDIT_NAME = "name"
    EDIT_CHAIN = "chain"
    VIEW = "view"
    SET_CHAIN = "set_chain"
    CHANGE_CHAIN = "edit_chain"
    BACK = "back"


class GroupCB(CallbackData, prefix="admin_group"):
    action: str
    group_id: int
    chain: str
