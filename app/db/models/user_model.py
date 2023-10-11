from tortoise import fields, models


class UserModel(models.Model):
    id = fields.BigIntField(pk=True)
    confirmed = fields.BooleanField(default=False)

    class Meta:
        fields = "__all__"

    def __str__(self):
        return str(self.id)
