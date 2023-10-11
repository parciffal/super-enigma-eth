from aiogram import Router, F  # , Bot
from aiogram.types import CallbackQuery  # , Message
from aiogram.fsm.context import FSMContext

import logging

from app.utils.cb_data.admin.menu_cb import AdminMenuCB, AdminMenuActions
from app.utils.cb_data.admin.ads_cb import AdsCB, AdsActions
from app.db.models import AdsModel

from .edit_ads import view_ads_cb

router = Router()


@router.callback_query(AdminMenuCB.filter(F.action == AdminMenuActions.ADD_ADS))
async def add_admin_ads_cb(
    query: CallbackQuery, callback_data: AdminMenuCB, state: FSMContext
):
    try:
        new_add = await AdsModel.create()
        await new_add.save()
        cb_data = AdsCB(action=AdsActions.SHOW_ADS, ads_id=new_add.id)
        await view_ads_cb(query, cb_data, state)
    except Exception as e:
        logging.error(e)
