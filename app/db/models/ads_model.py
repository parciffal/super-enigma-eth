from tortoise import fields, models


class AdsModel(models.Model):
    id = fields.IntField(pk=True)
    description = fields.TextField(default="")
    show = fields.BooleanField(default=True)
    admin = fields.ForeignKeyField("models.AdminModel", on_delete=fields.CASCADE)

    class Meta:
        fields = "__all__"

    async def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "show": self.show,
        }
