from tortoise import fields, Model

from aiogram.utils.text_decorations import html_decoration as hd
from aiogram.utils.markdown import hide_link


class LinkModel(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=256, default="")
    link = fields.CharField(max_length=512, default="")
    show = fields.BooleanField(default=True)
    image = fields.BooleanField(default=False)
    ads = fields.ForeignKeyField("models.AdsModel", on_delete=fields.CASCADE)

    class Meta:
        fields = "__all__"

    def get_link(self) -> str:
        if self.show:
            if self.image:
                return f" {hide_link(self.link)} "
            else:
                return f"<b> | 🔗 </b>{hd.link(self.name, self.link)}"
        else:
            return ""
