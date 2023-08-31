from dataclasses import dataclass

from app.db.models import GroupModel, AdsModel


@dataclass
class AdvertiseData:
    groups: list[GroupModel]
    ads: list[AdsModel]

    def __init__(self, groups: list[GroupModel], ads: list[AdsModel]):
        self.groups = groups
        self.ads = ads

    async def add_group(self, group: GroupModel):
        self.groups.append(group)

    async def add_ads(self, add: AdsModel):
        self.ads.append(add)

    async def rem_group(self, group: GroupModel):
        self.groups.remove(group)

    async def rem_ads(self, add: AdsModel):
        self.ads.remove(add)

    async def clear_data(self):
        self.groups = []
        self.ads = []

    async def update_data(self, group: list[GroupModel], ads: list[AdsModel]):
        self.groups = group
        self.ads = ads
