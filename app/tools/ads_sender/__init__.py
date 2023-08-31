import asyncio
import logging
import random
from asyncio import Task

from aiogram import exceptions, Bot
from aiogram.types import FSInputFile

from app.db.models import AdsModel, GroupModel, AdsFrequency, AdminModel
from .ads_dataclass import AdvertiseData

"""
    :ToDo
    +1) send ads by groups
    2) write algorithm that will choose ads for every group
    3)     
"""


async def fetch_ads():
    ads = await AdsModel.all()
    return ads


async def fetch_groups():
    groups = await GroupModel.all()
    return groups


async def send_message_with_delay(bot, group: GroupModel, ads: AdsModel):

    try:
        file = FSInputFile(ads.media)
        if ads.media != "":
            if str(ads.media).find("photo") != -1:
                await bot.send_photo(chat_id=group.telegram_id,
                                     photo=file,
                                     caption="Ads: "+ads.description,
                                     parse_mode="html")
            elif str(ads.media).find("video") != -1:
                await bot.send_video(chat_id=group.telegram_id,
                                     video=file,
                                     caption="Ads: "+ads.description,
                                     parse_mode="html")
            elif str(ads.media).find("gif") != -1:
                await bot.send_animation(chat_id=group.telegram_id,
                                         animation=file,
                                         caption="Ads: "+ads.description,
                                         parse_mode="html")

        else:
            await bot.send_message(chat_id=group.telegram_id,
                                   text="Ads: "+ads.description,)

    except exceptions.TelegramRetryAfter as e:
        print(f"Sleeping for {e.retry_after} seconds")
        await asyncio.sleep(e.retry_after)
        return await bot.send_message(group.telegram_id, ads.description)


async def ads_chooser(ads: list[AdsModel], group: GroupModel) -> AdsModel:
    for add in ads:
        if not await AdsFrequency.filter(ads=add, group=group).exists():
            ads_frequency = AdsFrequency(ads=add, group=group, ads_frequency=1)
            await ads_frequency.save()
            return add
        else:
            ads_frequency = await AdsFrequency.get(ads=add, group=group)
            if ads_frequency.frequency_capping <= 5:
                ads_frequency.frequency_capping += 1
                await ads_frequency.save()
                return add
            else:
                continue
    return random.choice(ads)


async def fill_data():
    groups = await fetch_groups()
    ads = await fetch_ads()
    return AdvertiseData(groups, ads)


async def message_sender_task(bot: Bot):
    await asyncio.sleep(5)
    logging.info("Ads system started")
    while True:
        try:
            admin = await AdminModel.all().first()

            if admin.show_adds:
                data = await fill_data()
                for group in data.groups:
                    add = await ads_chooser(data.ads, group)
                    await send_message_with_delay(bot, group, add)
            await asyncio.sleep(60)  # Adjust the interval as per your requirement
        except Exception as e:
            logging.error(e)
            await asyncio.sleep(15)
