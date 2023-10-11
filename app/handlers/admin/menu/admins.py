from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.utils.text_decorations import html_decoration as hd

from app.utils.cb_data.admin import AdminActions, AdminCB, AdminMenuActions, AdminMenuCB
from app.utils.states.admin.admin_state import AdminState
from app.db.models import AdminModel
from app.keyboards.inline.admin.admin_kb import get_all_admins, get_admins_actions_kb
from app.keyboards.inline.admin.group_kb import empty_kb
import logging


router = Router()


async def message_tamplate(admin):
    message = (
        f"<b>Username:</b> @{admin.username}\n"
        f"<b>Active:</b> {admin.active}\n"
        f"<b>Telegram id:</b> {hd.code(admin.telegram_id)}\n"
    )
    return message


@router.callback_query(AdminCB.filter(F.action == AdminActions.EDIT_ACTIVE))
async def edit_admin_active_cb(
    query: CallbackQuery, callback_data: AdminCB, state: FSMContext
):
    try:
        admin = await AdminModel.get(telegram_id=callback_data.admin_id)
        admin.active = not admin.active
        await admin.save()
        if query.message:
            await query.message.edit_text(await message_tamplate(admin))
            await query.message.edit_reply_markup(
                await get_admins_actions_kb(admin.telegram_id, admin.active)
            )
    except Exception as e:
        logging.error(repr(e))


@router.callback_query(AdminCB.filter(F.action == AdminActions.VIEW))
async def show_admin_cb(
    query: CallbackQuery, callback_data: AdminCB, state: FSMContext
):
    try:
        admin = await AdminModel.get(telegram_id=callback_data.admin_id)
        if query.message:
            print(1)
            await query.message.edit_text(await message_tamplate(admin))
            print(2)
            await query.message.edit_reply_markup(
                await get_admins_actions_kb(admin.telegram_id, admin.active)
            )
    except Exception as e:
        logging.error(repr(e))


@router.message(StateFilter(AdminState.link))
async def admin_link_message(message: Message, state: FSMContext, bot: Bot):
    try:
        if message.text:
            link = message.text
            group = await bot.get_chat(link)

            if not await AdminModel.filter(telegram_id=group.id).exists():
                grp = await AdminModel.create(
                    telegram_id=group.id,
                    username=group.username,
                )
                await grp.save()
        await state.clear()
        data = await AdminModel.all()
        if data:
            msg = "Choose admin to edit"
        else:
            msg = "No Admins"

        keyboard = await get_all_admins(data)
        await message.answer(msg, reply_markup=keyboard)
    except Exception as e:
        logging.error(repr(e))


@router.callback_query(AdminCB.filter(F.action == AdminActions.ADD))
async def admin_add_cb(query: CallbackQuery, callback_data: AdminCB, state: FSMContext):
    try:
        keyboard = await empty_kb()
        if query.message:
            await state.set_state(AdminState.link)
            await query.message.edit_text(
                "Send telegram_id of new admin\n"
            )
            await query.message.edit_reply_markup(keyboard)
    except Exception as e:
        logging.error(repr(e))


@router.callback_query(
    AdminMenuCB.filter(F.action == AdminMenuActions.ADMINS), StateFilter("*")
)
async def admin_admin_cb(
    query: CallbackQuery, callback_data: AdminMenuCB, state: FSMContext
):
    try:
        data = await AdminModel.all()
        if data:
            msg = "Choose admin to edit"
        else:
            msg = "No Admins"
        if query.message:
            keyboard = await get_all_admins(data)
            await query.message.edit_text(msg)
            await query.message.edit_reply_markup(keyboard)
    except Exception as e:
        logging.error(repr(e))
