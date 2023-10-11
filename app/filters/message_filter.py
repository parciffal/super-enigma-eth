from typing import Any, Union, Dict

from aiogram.filters import Filter
from aiogram.types import Message


class PrivateChatFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.chat.type == "private" and message.text.find("-") == -1


class GroupFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.chat.type != "private"
