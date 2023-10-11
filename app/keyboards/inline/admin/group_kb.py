from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.utils.cb_data.admin.group_cb import GroupActions, GroupCB
from app.utils.cb_data.admin.menu_cb import AdminMenuActions, AdminMenuCB
from app.db.models import GroupModel, ChatChain


async def edit_chain_kb(group_id) -> InlineKeyboardMarkup:
    buttons = []
    for i in ChatChain:
        print(i)
        buttons.append(
            InlineKeyboardButton(
                text=i.value,
                callback_data=GroupCB(
                    action=GroupActions.CHANGE_CHAIN, group_id=group_id, chain=i.value
                ).pack(),
            )
        )
    return InlineKeyboardMarkup(inline_keyboard=[buttons])


async def chain_kb(group_id) -> InlineKeyboardMarkup:
    buttons = []
    for i in ChatChain:
        print(i)
        buttons.append(
            InlineKeyboardButton(
                text=i.value,
                callback_data=GroupCB(
                    action=GroupActions.SET_CHAIN, group_id=group_id, chain=i.value
                ).pack(),
            )
        )
    return InlineKeyboardMarkup(inline_keyboard=[buttons])


async def empty_kb() -> InlineKeyboardMarkup:
    buttons: list = []
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def get_group_actions_kb(group_id: int, show: bool) -> InlineKeyboardMarkup:
    if show:
        show_btn = "🟢 Show"
    else:
        show_btn = "🔴 Show"
    buttons = [
        [
            InlineKeyboardButton(
                text=show_btn,
                callback_data=GroupCB(
                    action=GroupActions.EDIT_SHOW, group_id=group_id, chain=""
                ).pack(),
            ),
            InlineKeyboardButton(
                text="✏️  Chain",
                callback_data=GroupCB(
                    action=GroupActions.EDIT_CHAIN, group_id=group_id, chain=""
                ).pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text="⬅️  Back",
                callback_data=AdminMenuCB(action=AdminMenuActions.GROUPS).pack(),
            ),
            InlineKeyboardButton(
                text="🗑 Delete",
                callback_data=GroupCB(
                    action=GroupActions.DELETE, group_id=group_id, chain=""
                ).pack(),
            ),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def get_all_groups(groups: list[GroupModel]) -> InlineKeyboardMarkup:
    buttons = []
    for group in groups:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=group.title,
                    callback_data=GroupCB(
                        action=GroupActions.VIEW, group_id=group.telegram_id, chain=""
                    ).pack(),
                )
            ]
        )
    buttons.append(
        [
            InlineKeyboardButton(
                text="➕ Add",
                callback_data=GroupCB(
                    action=GroupActions.ADD, group_id=0, chain=""
                ).pack(),
            )
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
