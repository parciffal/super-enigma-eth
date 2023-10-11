from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.utils.cb_data.admin.ads_cb import AdsActions, AdsCB
from app.utils.cb_data.admin.view_ads_cb import ViewAdsActions, ViewAdsCB
from app.utils.cb_data.admin.menu_cb import AdminMenuActions, AdminMenuCB
from app.utils.cb_data.admin.links_cb import LinkActions, LinkCB


async def continue_view_kb(ads_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="◀️ Back",
                    callback_data=ViewAdsCB(
                        action=ViewAdsActions.BACK_TO_ADD, ads_id=ads_id
                    ).pack(),
                ),
                InlineKeyboardButton(
                    text="No media",
                    callback_data=ViewAdsCB(
                        action=ViewAdsActions.CONTINUE, ads_id=ads_id
                    ).pack(),
                ),
            ],
        ]
    )


async def ads_back_kb(ads_id: int, show) -> InlineKeyboardMarkup:
    if show:
        show_btn = "🟢 Show"
    else:
        show_btn = "🔴 Show"
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔗Links",
                    callback_data=LinkCB(
                        action=LinkActions.VIEW, ads_id=ads_id, link_id=0
                    ).pack(),
                ),
                InlineKeyboardButton(
                    text=show_btn,
                    callback_data=ViewAdsCB(
                        ads_id=ads_id,
                        action=ViewAdsActions.CHG_SHOW,
                    ).pack(),
                ),
            ],
            [
                InlineKeyboardButton(
                    text="✏️ Name",
                    callback_data=ViewAdsCB(
                        ads_id=ads_id,
                        action=ViewAdsActions.CHG_NAME,
                    ).pack(),
                ),
                InlineKeyboardButton(
                    text="✏️ Description",
                    callback_data=ViewAdsCB(
                        ads_id=ads_id,
                        action=ViewAdsActions.CHG_DESC,
                    ).pack(),
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🖼 Media",
                    callback_data=ViewAdsCB(
                        ads_id=ads_id,
                        action=ViewAdsActions.CHG_MEDIA,
                    ).pack(),
                ),
                InlineKeyboardButton(
                    text="🗑 Del",
                    callback_data=AdsCB(
                        ads_id=ads_id,
                        action=AdsActions.DELETE_ADS,
                    ).pack(),
                ),
            ],
            [
                InlineKeyboardButton(
                    text="◀️ Back",
                    callback_data=AdminMenuCB(
                        action=AdminMenuActions.ADS,
                    ).pack(),
                ),
                InlineKeyboardButton(
                    text="❌ Close",
                    callback_data=AdminMenuCB(action=AdminMenuActions.CLOSE).pack(),
                ),
            ],
        ]
    )
