from aiogram.filters.callback_data import CallbackData
from enum import Enum


class PaginationActions(str, Enum):
    JUMP = "jump"
    HERE = "here"


class PaginationCB(CallbackData, prefix="pagination"):
    action: PaginationActions
    page: int
