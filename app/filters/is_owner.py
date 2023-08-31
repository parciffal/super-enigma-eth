from aiogram import types
from aiogram.filters import Filter

from app.config import Config
from app.db.models import AdminModel


class IsOwner(Filter):
    async def __call__(
        self, message: types.Message, config: Config, *args, **kwargs
    ) -> bool:
        if (
            await AdminModel.filter(telegram_id=message.from_user.id)
            .filter(active=True)
            .exists()
        ):
            return True
        return message.from_user.id == config.settings.owner_id


class PrivateChatFilter(Filter):
    async def __call__(self, message: types.Message) -> bool:
        return message.chat.type == "private" and message.text.find("-") == -1
