import os
import aiofiles
from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, Message, ContentType, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.utils.text_decorations import html_decoration as hd


from app.db.models import AdsModel
from app.utils.cb_data.admin.ads_cb import AdsActions, AdsCB
from app.utils.cb_data.admin.menu_cb import AdminMenuCB, AdminMenuActions
from app.utils.cb_data.admin.view_ads_cb import ViewAdsCB, ViewAdsActions
from app.utils.states.admin.edit_ads_state import EditAdsState
from app.keyboards.inline.admin.ads_kb import ads_back_kb, continue_view_kb
from .show_ads import admin_ads_cb

import logging


router = Router()


async def del_media(media):
    try:
        file_name = os.path.realpath(media)
        os.remove(file_name)
        return True
    except FileNotFoundError:
        return False


async def prepare_ads_text(ads: AdsModel):
    return (
        f"<b>Ads info</b>\n"
        f"<b>Name</b>: {ads.name}\n"
        f"<b>Description</b>: {ads.description}\n"
        f"<b>Show</b>: {ads.show}"
        f'<a href="{ads.media}">&#8203;</a>'
    )


async def edit_ads_view(message, state: FSMContext, ads: AdsModel):
    text = await prepare_ads_text(ads)
    await state.clear()
    await message.delete()
    await message.answer(
        text, parse_mode="html", reply_markup=await ads_back_kb(ads.id, ads.show)
    )
    # if str(ads.media) == "":
    #     await message.delete()
    #     await message.answer(
    #         text, parse_mode="html", reply_markup=await ads_back_kb(ads.id, ads.show)
    #     )
    # else:
    #     file = FSInputFile(ads.media)
    #     if str(ads.media).find("photo") != -1:
    #         await message.delete()
    #         await message.answer_photo(
    #             photo=file,
    #             caption=text,
    #             parse_mode="html",
    #             reply_markup=await ads_back_kb(ads.id, ads.show),
    #         )
    #     elif str(ads.media).find("video") != -1:
    #         await message.delete()
    #         await message.answer_video(
    #             video=file,
    #             caption=text,
    #             parse_mode="html",
    #             reply_markup=await ads_back_kb(ads.id, ads.show),
    #         )
    #     elif str(ads.media).find("gif") != -1:
    #         await message.delete()
    #         await message.answer_animation(
    #             animation=file,
    #             caption=text,
    #             parse_mode="html",
    #             reply_markup=await ads_back_kb(ads.id, ads.show),
    #         )
    #     else:
    #         pass


@router.message(
    StateFilter(EditAdsState.ads_media),
    F.content_type.in_(
        [ContentType.TEXT]),
)
async def view_ads_chg_media_mess(message: Message, bot: Bot, state: FSMContext):
    try:
        data = await state.get_data()
        #
        # if message.photo is not None:
        #     destination_path = (
        #         f"app/media/admin/photo/{message.photo[-1].file_unique_id}.png"
        #     )
        #     file_id = message.photo[-1].file_id
        # elif message.video is not None:
        #     file_id = message.video.file_id
        #     destination_path = (
        #         f"app/media/admin/video/{message.video.file_unique_id}.mp4"
        #     )
        # elif message.animation is not None:
        #     file_id = message.animation.file_id
        #     destination_path = (
        #         f"app/media/admin/gif/{message.animation.file_unique_id}.gif.mp4"
        #     )
        # else:
        #     await state.set_state(EditAdsState.ads_media)
        #     await message.answer(
        #         text="Something's wrong resend media \n"
        #         "it should be` photo, video(0-60 seconds), gif"
        #     )
        # file = await bot.get_file(file_id)
        # print(destination_path)
        # file_save = await bot.download(file, destination_path)
        # print(file_save)
        ads = await AdsModel.get(id=data["ads_id"])
        # if ads.media != "":
        #     await del_media(ads.media)
        ads.media = message.text
        await ads.save()
        await state.clear()
        await edit_ads_view(message, state, ads)
    except Exception as e:
        logging.error(e)


@router.callback_query(
    ViewAdsCB.filter(F.action == ViewAdsActions.CONTINUE), StateFilter("*")
)
async def view_ads_no_media(
    query: CallbackQuery, callback_data: ViewAdsCB, state: FSMContext, bot: Bot
):
    try:
        await state.clear()
        ads = await AdsModel.get(id=callback_data.ads_id)
        if ads.media != "":
            # await del_media(ads.media)
            ads.media = ""
            await ads.save()
        await edit_ads_view(query.message, state, ads)
    except Exception as e:
        logging.error(e)


@router.callback_query(ViewAdsCB.filter(F.action == ViewAdsActions.CHG_MEDIA))
async def view_ads_chg_media(
    query: CallbackQuery, callback_data: ViewAdsCB, state: FSMContext
):
    try:
        print("")
        data = await state.get_data()
        data["ads_id"] = callback_data.ads_id
        await state.set_data(data)
        await state.set_state(EditAdsState.ads_media)
        if query.message:
            await query.message.delete()
            await query.message.answer(
                "Ok now send media url of ads\n",
                reply_markup=await continue_view_kb(callback_data.ads_id),
            )
    except Exception as e:
        logging.error(e)


@router.callback_query(ViewAdsCB.filter(F.action == ViewAdsActions.CHG_SHOW))
async def view_ads_show(
    query: CallbackQuery, callback_data: ViewAdsCB, state: FSMContext
):
    try:
        ads = await AdsModel.get(id=callback_data.ads_id)
        ads.show = not ads.show
        await ads.save()
        await edit_ads_view(query.message, state, ads)
    except Exception as e:
        logging.error(e)


@router.callback_query(AdsCB.filter(F.action == AdsActions.DELETE_ADS))
async def view_ads_delete(
    query: CallbackQuery, callback_data: AdsCB, state: FSMContext
):
    try:
        ads = await AdsModel.get(id=callback_data.ads_id)
        if ads.media != "":
            await del_media(ads.media)
        await ads.delete()
        await admin_ads_cb(
            query,
            AdminMenuCB(action=AdminMenuActions.ADS),
            state,
        )
    except Exception as e:
        logging.error(e)


@router.message(
    F.content_type.in_({ContentType.TEXT}), StateFilter(
        EditAdsState.ads_description)
)
async def view_ads_chg_desc_msg(message: Message, state: FSMContext, bot: Bot):
    try:
        data = await state.get_data()
        ads = await AdsModel.get(id=data["ads_id"])
        ads.description = message.text if message.text else ""
        await ads.save()
        await state.clear()
        await bot.delete_message(message.chat.id, message.message_id - 1)
        await edit_ads_view(message, state, ads)
    except Exception as e:
        logging.error(e)


@router.callback_query(ViewAdsCB.filter(F.action == ViewAdsActions.CHG_DESC))
async def view_ads_chg_description(
    query: CallbackQuery, callback_data: ViewAdsCB, state: FSMContext
):
    try:
        await state.set_state(EditAdsState.ads_description)
        data = await state.get_data()
        data["ads_id"] = callback_data.ads_id
        await state.set_data(data)
        if query.message:
            await query.message.delete()
            await query.message.answer("Send new description of ads or /cancel")
    except Exception as e:
        logging.error(e)


@router.message(
    F.content_type.in_({ContentType.TEXT}), StateFilter(EditAdsState.ads_name)
)
async def view_ads_chg_name_msg(message: Message, state: FSMContext, bot: Bot):
    try:
        data = await state.get_data()
        ads = await AdsModel.get(id=data["ads_id"])
        ads.name = message.text if message.text else ""
        await ads.save()
        await state.clear()
        await bot.delete_message(message.chat.id, message.message_id - 1)
        await edit_ads_view(message, state, ads)
    except Exception as e:
        logging.error(e)


@router.callback_query(ViewAdsCB.filter(F.action == ViewAdsActions.CHG_NAME))
async def view_ads_chg_name(
    query: CallbackQuery, callback_data: ViewAdsCB, state: FSMContext
):
    try:
        await state.set_state(EditAdsState.ads_name)
        data = await state.get_data()
        data["ads_id"] = callback_data.ads_id
        await state.set_data(data)
        if query.message:
            await query.message.delete()
            await query.message.answer("Send new name of ads or /cancel")
    except Exception as e:
        logging.error(e)


@router.callback_query(AdsCB.filter(F.action == AdsActions.SHOW_ADS))
async def view_ads_cb(query: CallbackQuery, callback_data: AdsCB, state: FSMContext):
    try:
        ads = await AdsModel.get(id=callback_data.ads_id)
        await edit_ads_view(query.message, state, ads)
    except Exception as e:
        logging.error(e)
