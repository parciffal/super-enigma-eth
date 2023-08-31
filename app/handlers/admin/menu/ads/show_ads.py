from aiogram import Router, F  # , Bot
from aiogram.types import CallbackQuery  # , Message
from aiogram.fsm.context import FSMContext

import logging

from app.utils.cb_data.admin.pagination_cb import PaginationCB, PaginationActions
from app.utils.cb_data.admin.menu_cb import AdminMenuCB, AdminMenuActions
from app.keyboards.inline.admin.pagination_kb import ads_pagination

router = Router()


@router.callback_query(PaginationCB.filter(F.action == PaginationActions.JUMP))
async def pagination_cb(
    query: CallbackQuery, callback_data: PaginationCB, state: FSMContext
):
    try:
        data = await state.get_data()
        data["page"] = callback_data.page
        await state.set_data(data)
        page = await ads_pagination(data["admin"], data["page"])
        await state.set_data(data)
        await query.message.edit_reply_markup(page)
    except Exception as e:
        logging.error(e)


@router.callback_query(AdminMenuCB.filter(F.action == AdminMenuActions.ADS))
async def admin_ads_cb(
    query: CallbackQuery, callback_data: AdminMenuCB, state: FSMContext
):
    try:
        data = await state.get_data()
        if data.get("page"):
            page = await ads_pagination(data["page"])
        else:
            page = await ads_pagination()
        if query.message:
            await query.message.delete()
            await query.message.answer("Ads list", reply_markup=page)
    except Exception as e:
        logging.error(e)
