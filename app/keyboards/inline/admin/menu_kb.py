from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.utils.cb_data.admin.menu_cb import AdminMenuActions, AdminMenuCB


async def start_menu() -> InlineKeyboardMarkup:
    buttons = []
    for i in AdminMenuActions:
        buttons.append(
            [InlineKeyboardButton(text=i, callback_data=AdminMenuCB(action=i).pack())]
        )

    return InlineKeyboardMarkup(inline_keyboard=[*buttons])
