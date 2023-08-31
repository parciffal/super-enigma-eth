from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.utils.text_decorations import html_decoration as hd

from app.keyboards.inline.admin.group_kb import (
    get_all_groups,
    get_group_actions_kb,
    empty_kb,
    chain_kb,
    edit_chain_kb,
)
from app.utils.cb_data.admin.menu_cb import AdminMenuCB, AdminMenuActions
from app.utils.cb_data.admin.group_cb import GroupActions, GroupCB
from app.utils.states.admin import GroupState
from app.db.models import GroupModel
import logging


router = Router()


async def message_tamplate(group):
    message = (
        f"<b>Username:</b> @{group.name}\n"
        f"<b>Title:</b> {group.title}\n"
        f"<b>Link:</b> {group.link}\n"
        f"<b>Chain:</b> {group.chain}\n"
        f"<b>Show:</b> {group.show}\n"
        f"<b>Telegram id:</b> {hd.code(group.telegram_id)}\n"
    )
    return message


@router.callback_query(GroupCB.filter(F.action == GroupActions.SET_CHAIN))
async def set_group_chain(
    query: CallbackQuery, callback_data: GroupCB, state: FSMContext
):
    try:
        group = await GroupModel.get(telegram_id=callback_data.group_id)
        group.chain = callback_data.chain
        await group.save()
        await state.clear()
        groups = await GroupModel.all()
        keyboard = await get_all_groups(groups)
        if query.message:
            await query.message.answer("Group Added/Edited", reply_markup=keyboard)
    except Exception as e:
        logging.error(repr(e))


@router.message(StateFilter(GroupState.link))
async def group_link_message(message: Message, state: FSMContext, bot: Bot):
    try:
        if message.text:
            link = message.text
            if "https://t.me/" in link:
                link = link.replace("https://t.me/", "@")
            group = await bot.get_chat(link)
            username = group.username
            title = group.title
            telegram_id = group.id
            link = f"https://t.me/{username}"
            if not await GroupModel.filter(telegram_id=telegram_id).exists():
                grp = await GroupModel.create(
                    telegram_id=telegram_id,
                    name=username,
                    title=title,
                    link=link,
                )
                await grp.save()
            await state.clear()
            keyboard = await chain_kb(grp.telegram_id)
            await message.answer("Choose chain of group", reply_markup=keyboard)
        else:
            await state.clear()
    except Exception as e:
        logging.error(repr(e))


@router.callback_query(GroupCB.filter(F.action == GroupActions.ADD))
async def add_group_cb(query: CallbackQuery, callback_data: GroupCB, state: FSMContext):
    try:
        keyboard = await empty_kb()
        if query.message:
            await state.set_state(GroupState.link)
            await query.message.edit_text("Send group/chat link")
            await query.message.edit_reply_markup(keyboard)
    except Exception as e:
        logging.error(repr(e))


@router.callback_query(GroupCB.filter(F.action == GroupActions.DELETE))
async def delete_group_cb(
    query: CallbackQuery, callback_data: GroupCB, state: FSMContext
):
    try:
        group = await GroupModel.get(telegram_id=callback_data.group_id)
        await group.delete()
        data = await GroupModel.all()
        if data:
            msg = "Choose group to edit"
        else:
            msg = "No groups"
        if query.message:
            keyboard = await get_all_groups(data)
            await query.message.edit_text(msg)
            await query.message.edit_reply_markup(keyboard)
    except Exception as e:
        logging.error(e)


@router.callback_query(GroupCB.filter(F.action == GroupActions.CHANGE_CHAIN))
async def change_group_chain(
    query: CallbackQuery, callback_data: GroupCB, state: FSMContext
):
    try:
        group = await GroupModel.get(telegram_id=callback_data.group_id)
        group.chain = callback_data.chain
        await group.save()
        await state.clear()
        if query.message:
            await query.message.edit_text(await message_tamplate(group))
            await query.message.edit_reply_markup(
                await get_group_actions_kb(group.telegram_id, group.show)
            )
    except Exception as e:
        logging.error(repr(e))


@router.callback_query(GroupCB.filter(F.action == GroupActions.EDIT_CHAIN))
async def edit_chain_group_cb(
    query: CallbackQuery, callback_data: GroupCB, state: FSMContext
):
    try:
        group = await GroupModel.get(telegram_id=callback_data.group_id)
        group.chain = callback_data.chain
        await group.save()
        if query.message:
            await query.message.edit_text(await message_tamplate(group))
            await query.message.edit_reply_markup(
                await edit_chain_kb(group.telegram_id)
            )
    except Exception as e:
        logging.error(e)


@router.callback_query(GroupCB.filter(F.action == GroupActions.EDIT_SHOW))
async def edit_show_group_cb(
    query: CallbackQuery, callback_data: GroupCB, state: FSMContext
):
    try:
        group = await GroupModel.get(telegram_id=callback_data.group_id)
        group.show = not group.show
        await group.save()
        if query.message:
            await query.message.edit_text(await message_tamplate(group))
            await query.message.edit_reply_markup(
                await get_group_actions_kb(group.telegram_id, group.show)
            )
    except Exception as e:
        logging.error(e)


@router.callback_query(GroupCB.filter(F.action == GroupActions.VIEW))
async def show_group_cb(
    query: CallbackQuery, callback_data: GroupCB, state: FSMContext
):
    try:
        group = await GroupModel.get(telegram_id=callback_data.group_id)
        if query.message:
            await query.message.edit_text(await message_tamplate(group))
            await query.message.edit_reply_markup(
                await get_group_actions_kb(group.telegram_id, group.show)
            )
    except Exception as e:
        logging.error(repr(e))


@router.callback_query(
    AdminMenuCB.filter(F.action == AdminMenuActions.GROUPS), StateFilter("*")
)
async def admin_group_cb(
    query: CallbackQuery, callback_data: AdminMenuCB, state: FSMContext
):
    try:
        data = await GroupModel.all()
        if data:
            msg = "Choose group to edit"
        else:
            msg = "No groups"
        if query.message:
            keyboard = await get_all_groups(data)
            await query.message.edit_text(msg)
            await query.message.edit_reply_markup(keyboard)
    except Exception as e:
        logging.error(repr(e))
