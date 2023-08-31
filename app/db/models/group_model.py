from enum import Enum

from tortoise import fields, models
from aiogram.utils.text_decorations import html_decoration as hd


class ChatChain(str, Enum):
    BTC = "btc"
    ETH = "eth"


class GroupModel(models.Model):
    telegram_id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=256, default="")
    title = fields.CharField(max_length=256, default="")
    link = fields.CharField(max_length=512, default="")
    show = fields.BooleanField(default=True)
    chain = fields.CharField(max_length=256, default="btc")

    class Meta:
        fields = "__all__"

    async def to_dict(self) -> dict:
        return {
            "id": self.telegram_id,
            "name": self.name,
            "title": self.title,
            "link": self.link,
            "show": self.show,
            "chain": self.chain,
        }

    async def to_link(self) -> str:
        return f"👥 {hd.link(self.title, self.link)}"
