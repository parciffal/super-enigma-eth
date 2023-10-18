from tortoise import fields, models


class GroupModel(models.Model):
    telegram_id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=256, default="")
    show = fields.BooleanField(default=True)

    class Meta:
        fields = "__all__"

    async def to_dict(self) -> dict:
        return {
            "id": self.telegram_id,
            "name": self.name,
            "show": self.show,
        }
