from enum import Enum

from tortoise import fields, models


class ChatChain(Enum):
    BTC = "btc"
    ETH = "eth"


class GroupModel(models.Model):
    telegram_id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=256, default="")
    link = fields.CharField(max_length=512, default="")
    show = fields.BooleanField(default=True)
    chain = fields.CharEnumField(ChatChain, default=ChatChain.BTC)

    class Meta:
        fields = "__all__"

    async def to_dict(self) -> dict:
        return {
            "id": self.telegram_id,
            "name": self.name,
            "link": self.link,
            "show": self.show,
            "chain": self.chain,
        }
