from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.db.models import LinkModel
from app.utils.cb_data.admin.links_cb import LinkActions, LinkCB
from app.utils.cb_data.admin.menu_cb import AdminMenuActions, AdminMenuCB
from app.utils.cb_data.admin.ads_cb import AdsCB, AdsActions


#
async def link_view_kb(link: LinkModel, callback_data: LinkCB) -> InlineKeyboardMarkup:
    show = "🔴 Show"
    if link.show:
        show = "🟢 Show"
    image = "🔴 Image"
    if link.image:
        image = "🟢 Image"
    buttons = [
        [
            InlineKeyboardButton(
                text="✏️ Name",
                callback_data=LinkCB(
                    action=LinkActions.NAME,
                    ads_id=callback_data.ads_id,
                    link_id=link.id,
                ).pack(),
            ),
            InlineKeyboardButton(
                text="✏️ Link",
                callback_data=LinkCB(
                    action=LinkActions.LINK,
                    ads_id=callback_data.ads_id,
                    link_id=link.id,
                ).pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text=image,
                callback_data=LinkCB(
                    action=LinkActions.IMAGE,
                    ads_id=callback_data.ads_id,
                    link_id=link.id,
                ).pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text=show,
                callback_data=LinkCB(
                    action=LinkActions.EDIT_SHOW,
                    ads_id=callback_data.ads_id,
                    link_id=link.id,
                ).pack(),
            ),
            InlineKeyboardButton(
                text="🗑 Delete",
                callback_data=LinkCB(
                    action=LinkActions.DELETE,
                    ads_id=callback_data.ads_id,
                    link_id=link.id,
                ).pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text="⬅️  Back",
                callback_data=LinkCB(
                    action=LinkActions.VIEW, ads_id=callback_data.ads_id, link_id=0
                ).pack(),
            ),
            InlineKeyboardButton(
                text="❌ Close",
                callback_data=AdminMenuCB(action=AdminMenuActions.CLOSE).pack(),
            ),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


#
async def get_all_links(links: list[LinkModel], ads_id) -> InlineKeyboardMarkup:
    buttons = []
    for link in links:
        name = link.name if link.name != "" else str(link.id)
        buttons.append(
            [
                InlineKeyboardButton(
                    text=name,
                    callback_data=LinkCB(
                        action=LinkActions.SHOW, ads_id=ads_id, link_id=link.id
                    ).pack(),
                )
            ]
        )
    buttons.append(
        [
            InlineKeyboardButton(
                text="➕ Add",
                callback_data=LinkCB(
                    action=LinkActions.ADD, ads_id=ads_id, link_id=0
                ).pack(),
            )
        ]
    )
    buttons.append(
        [
            InlineKeyboardButton(
                text="⬅️  Back",
                callback_data=AdsCB(action=AdsActions.SHOW_ADS, ads_id=ads_id).pack(),
            ),
            InlineKeyboardButton(
                text="❌ Close",
                callback_data=AdminMenuCB(action=AdminMenuActions.CLOSE).pack(),
            ),
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=buttons)
