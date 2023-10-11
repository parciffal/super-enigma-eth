from tortoise import fields, models


class AdsModel(models.Model):
    id = fields.IntField(pk=True)
    name = fields.TextField(default="")
    description = fields.TextField(default="")
    media = fields.TextField(default="")
    show = fields.BooleanField(default=False)

    class Meta:
        fields = "__all__"

    async def ads_to_message(self):
        return f"📣 <b>{self.name}: {self.description}</b>"
