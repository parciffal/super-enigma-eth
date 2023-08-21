from tortoise import fields, models


class AdminModel(models.Model):
    telegram_id = fields.BigIntField(pk=True)

    class Meta:
        fields = "__all__"

    async def to_dict(self) -> dict:
        return {"telegram_id": self.telegram_id}
