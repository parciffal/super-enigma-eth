from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.utils.cb_data.admin import AdminActions, AdminCB, AdminMenuActions, AdminMenuCB
from app.db.models import AdminModel


async def get_admins_actions_kb(admin_id: int, active: bool) -> InlineKeyboardMarkup:
    if active:
        show_btn = "🟢 Active"
    else:
        show_btn = "🔴 Active"
    buttons = [
        [
            InlineKeyboardButton(
                text=show_btn,
                callback_data=AdminCB(
                    action=AdminActions.EDIT_ACTIVE, admin_id=admin_id
                ).pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text="⬅️  Back",
                callback_data=AdminMenuCB(action=AdminMenuActions.ADMINS).pack(),
            ),
            InlineKeyboardButton(
                text="🗑 Delete",
                callback_data=AdminCB(
                    action=AdminActions.DELETE, admin_id=admin_id
                ).pack(),
            ),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def get_all_admins(admins: list[AdminModel]) -> InlineKeyboardMarkup:
    buttons = []
    for admin in admins:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=admin.username,
                    callback_data=AdminCB(
                        action=AdminActions.VIEW, admin_id=admin.telegram_id
                    ).pack(),
                )
            ]
        )
    buttons.append(
        [
            InlineKeyboardButton(
                text="➕ Add",
                callback_data=AdminCB(action=AdminActions.ADD, admin_id=0).pack(),
            ),
        ]
    )
    buttons.append(
        [
            InlineKeyboardButton(
                text="⬅️  Back",
                callback_data=AdminMenuCB(action=AdminMenuActions.BACK).pack(),
            ),
            InlineKeyboardButton(
                text="❌ Close",
                callback_data=AdminMenuCB(action=AdminMenuActions.CLOSE).pack(),
            ),
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=[*buttons])
