from aiogram import Bot
from aiogram.types import FSInputFile

from app.db.models import AdsModel, LinkModel


class AdsManager:
    def __init__(self):
        self.last_ads_id = None

    async def get_filtered_ads(self):
        if self.last_ads_id is None:
            ads = await AdsModel.all().filter(show=True).order_by("id")
            if ads:
                self.last_ads_id = ads[0].id
                return ads[0]
            else:
                return None

        ads = (
            await AdsModel.filter(id__gt=self.last_ads_id)
            .filter(show=True)
            .order_by("id")
            .first()
        )
        if ads is None:
            # If no ads with id greater than last_ads_id, start from the beginning
            ads = (
                await AdsModel.filter(show=True)
                .filter(show=True)
                .order_by("id")
                .first()
            )
        self.last_ads_id = ads.id
        return ads

    async def get_ads_links(self, ads: AdsModel):
        links = await LinkModel.filter(ads=ads)
        if links:
            return links
        else:
            return []

    async def ads_links_to_str(
        self, ads: AdsModel, links: list[LinkModel], bot: Bot
    ) -> str:
        links = [i.get_link() for i in links]
        message = await ads.ads_to_message()
        for i in links:
            message += i
        return message

    async def get_ads(self, bot: Bot):
        try:
            ads = await self.get_filtered_ads()
            if ads is not None:
                links = await self.get_ads_links(ads)
                msg = await self.ads_links_to_str(ads, links, bot)
                media = f'<a href="{ads.media}">&#8203;</a>'
                return msg, media
            else:
                return ""
        except:
            return ""


ads_manager = AdsManager()
