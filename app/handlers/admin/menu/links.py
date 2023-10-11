from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from app.utils.cb_data.admin.menu_cb import AdminMenuCB, AdminMenuActions
from app.utils.cb_data.admin.links_cb import LinkActions, LinkCB
from app.keyboards.inline.admin.link_kb import get_all_links, link_view_kb
from app.utils.states.admin.link_state import LinkState
from app.db.models import LinkModel, AdsModel
import logging


router = Router()


async def link_view_message(
    query: CallbackQuery, link: LinkModel, callback_data: LinkCB
):
    msg = f"<b>Link info</b>\n<b>Name:</b> {link.name}\n<b>Link:</b> {link.link}\n"
    keyboard = await link_view_kb(link, callback_data)
    if query.message:
        try:
            await query.message.edit_text(msg)
        except Exception as e:
            logging.error(e)
            await query.message.edit_caption(msg)
        await query.message.edit_reply_markup(keyboard)


async def link_changed_message(
    message: Message, link: LinkModel, callback_data: LinkCB, bot: Bot
):
    msg = f"<b>Link info</b>\n<b>Name:</b> {link.name}\n<b>Link:</b> {link.link}\n"
    keyboard = await link_view_kb(link, callback_data)
    await message.delete()
    message_id = message.message_id - 1
    chat_id = message.chat.id
    if message:
        try:
            await bot.edit_message_text(msg, chat_id=chat_id, message_id=message_id)
        except Exception as e:
            logging.error(e)
            await bot.edit_message_caption(chat_id, message_id, caption=msg)
        await bot.edit_message_reply_markup(chat_id, message_id, reply_markup=keyboard)


@router.message(F.content_type.in_({ContentType.TEXT}), StateFilter(LinkState.name))
async def ads_link_name_msg(message: Message, state: FSMContext, bot: Bot):
    try:
        data = await state.get_data()
        link = await LinkModel.get(id=data["callback_data"].link_id)
        link.name = message.text if message.text else ""
        await link.save()
        await state.clear()
        await link_changed_message(message, link, data["callback_data"], bot)
    except Exception as e:
        logging.error(e)


@router.callback_query(LinkCB.filter(F.action == LinkActions.NAME))
async def ads_link_name_cb(
    query: CallbackQuery, callback_data: LinkCB, state: FSMContext
):
    try:
        await state.set_state(LinkState.name)
        data = await state.get_data()
        data["callback_data"] = callback_data
        await state.set_data(data)
        if query.message:
            await query.message.delete()
            await query.message.answer("Send Link Name or /cancel")
    except Exception as e:
        logging.error(e)


@router.message(F.content_type.in_({ContentType.TEXT}), StateFilter(LinkState.link))
async def ads_link_link_msg(message: Message, state: FSMContext, bot: Bot):
    try:
        data = await state.get_data()
        link = await LinkModel.get(id=data["callback_data"].link_id)
        link.link = message.text if message.text else ""
        await link.save()
        await state.clear()
        await link_changed_message(message, link, data["callback_data"], bot)
    except Exception as e:
        logging.error(e)


@router.callback_query(LinkCB.filter(F.action == LinkActions.LINK))
async def ads_link_link_cb(
    query: CallbackQuery, callback_data: LinkCB, state: FSMContext
):
    try:
        await state.set_state(LinkState.link)
        data = await state.get_data()
        data["callback_data"] = callback_data
        await state.set_data(data)
        if query.message:
            await query.message.delete()
            await query.message.answer("Send Link Link or /cancel")
    except Exception as e:
        logging.error(e)


@router.callback_query(LinkCB.filter(F.action == LinkActions.ADD))
async def ads_link_add_cb(
    query: CallbackQuery, callback_data: LinkCB, state: FSMContext
):
    try:
        ads = await AdsModel.get(id=callback_data.ads_id)
        link = await LinkModel.create(ads=ads)
        await link_view_message(query, link, callback_data)
    except Exception as e:
        logging.error(e)


@router.callback_query(LinkCB.filter(F.action == LinkActions.SHOW))
async def ads_link_show_cb(
    query: CallbackQuery, callback_data: LinkCB, state: FSMContext
):
    try:
        link = await LinkModel.get(id=callback_data.link_id)
        await link_view_message(query, link, callback_data)
    except Exception as e:
        logging.error(e)


@router.callback_query(LinkCB.filter(F.action == LinkActions.DELETE))
async def ads_link_delete_cb(
    query: CallbackQuery, callback_data: LinkCB, state: FSMContext
):
    try:
        link = await LinkModel.get(id=callback_data.link_id)
        await link.delete()
        await ads_link_cb(query, callback_data, state)
    except Exception as e:
        logging.error(e)


@router.callback_query(LinkCB.filter(F.action == LinkActions.EDIT_SHOW))
async def ads_link_edit_show_cb(
    query: CallbackQuery, callback_data: LinkCB, state: FSMContext
):
    try:
        link = await LinkModel.get(id=callback_data.link_id)
        link.show = not link.show
        await link.save()
        await link_view_message(query, link, callback_data)
    except Exception as e:
        logging.error(e)


@router.callback_query(LinkCB.filter(F.action == LinkActions.IMAGE))
async def ads_link_image_cb(
    query: CallbackQuery, callback_data: LinkCB, state: FSMContext
):
    try:
        link = await LinkModel.get(id=callback_data.link_id)
        link.image = not link.image
        await link.save()
        await link_view_message(query, link, callback_data)
    except Exception as e:
        logging.error(e)


@router.callback_query(LinkCB.filter(F.action == LinkActions.VIEW))
async def ads_link_cb(query: CallbackQuery, callback_data: LinkCB, state: FSMContext):
    try:
        ads = await AdsModel.get(id=callback_data.ads_id)
        links = await LinkModel.filter(ads=ads)
        if links:
            msg = "Choose link to edit"
        else:
            msg = "No link"
        if query.message:
            keyboard = await get_all_links(links, callback_data.ads_id)
            try:
                await query.message.edit_caption(msg)
            except Exception as e:
                logging.error(e)
                await query.message.edit_text(msg)
            await query.message.edit_reply_markup(keyboard)
    except Exception as e:
        logging.error(repr(e))
