from aiogram.filters.callback_data import CallbackData

from enum import Enum


#
class LinkActions(str, Enum):
    ADD = "add"
    DELETE = "delete"
    NAME = "name"
    LINK = "link"
    VIEW = "view"
    SHOW = "show"
    EDIT_SHOW = "edit_show"
    IMAGE = "image"


#
class LinkCB(CallbackData, prefix="group_link"):
    action: str
    ads_id: int
    link_id: int
