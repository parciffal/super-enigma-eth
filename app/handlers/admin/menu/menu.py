#
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

#
from app.keyboards.inline.admin.menu_kb import start_menu
from app.filters.is_owner import IsOwner
from app.utils.cb_data.admin import AdminMenuCB, AdminMenuActions
from app.filters.is_owner import PrivateChatFilter
import logging


router = Router()


@router.callback_query(
    AdminMenuCB.filter(F.action == AdminMenuActions.CLOSE), StateFilter("*")
)
async def admin_menu_close_cb(
    query: CallbackQuery, callback_data: AdminMenuCB, state: FSMContext
):
    try:
        await state.clear()
        if query.message:
            await query.message.delete()
    except Exception as e:
        logging.error(repr(e))


@router.callback_query(
    AdminMenuCB.filter(F.action == AdminMenuActions.BACK), StateFilter("*")
)
async def admin_back_cb(
    query: CallbackQuery, callback_data: AdminMenuCB, state: FSMContext
):
    try:
        await state.clear()
        if query.message:
            await query.message.delete()
            keyboard = await start_menu()
            await query.message.answer(
                text="Select section to edit", reply_markup=keyboard
            )
    except Exception as e:
        logging.error(e)


@router.message(Command("cancel"), StateFilter("*"))
async def admin_cancel_cmd(message: Message, state: FSMContext):
    try:
        await state.clear()
        if message:
            await message.delete()
            await admin_menu_cmd(message)
    except Exception as e:
        logging.error(e)


@router.message(Command("admin"), StateFilter("*"), IsOwner(), PrivateChatFilter())
async def admin_menu_cmd(message: Message):
    try:
        keyboard = await start_menu()
        await message.delete()
        await message.answer("Select section to edit", reply_markup=keyboard)
    except Exception as e:
        logging.error(e)
