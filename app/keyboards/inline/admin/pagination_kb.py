from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tortoise.queryset import QuerySet

from app.db.models import AdsModel
from app.utils.cb_data.admin.pagination_cb import PaginationActions, PaginationCB
from app.utils.cb_data.admin.ads_cb import AdsActions, AdsCB
from app.utils.cb_data.admin.menu_cb import AdminMenuCB, AdminMenuActions


async def generate_ads_keyboard(ads, position, pages) -> InlineKeyboardMarkup:
    back_buttons = [
        InlineKeyboardButton(
            text="⬅️  Back",
            callback_data=AdminMenuCB(
                action=AdminMenuActions.BACK,
            ).pack(),
        ),
        InlineKeyboardButton(
            text="❌ Close",
            callback_data=AdminMenuCB(action=AdminMenuActions.CLOSE).pack(),
        ),
    ]
    add_button = [
        InlineKeyboardButton(
            text="➕ Ads",
            callback_data=AdminMenuCB(action=AdminMenuActions.ADD_ADS).pack(),
        )
    ]
    if pages == 0:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="➕ Ads",
                        callback_data=AdminMenuCB(
                            action=AdminMenuActions.ADD_ADS
                        ).pack(),
                    )
                ],
                back_buttons,
            ]
        )
    else:
        ads_buttons = [
            [
                InlineKeyboardButton(
                    text=i.name if i.name != "" else str(i.id),
                    callback_data=AdsCB(
                        action=AdsActions.SHOW_ADS,
                        ads_id=i.id,
                    ).pack(),
                )
            ]
            for i in ads
        ]
        page_buttons = []
        if 1 <= position <= round(pages):
            start = 1
            end = round(pages)
        else:
            start = position - 2
            end = position + 2
        for i in range(start, end + 1):
            if i == position:
                page_buttons.append(
                    InlineKeyboardButton(
                        text=f"-{i}-",
                        callback_data=PaginationCB(
                            action=PaginationActions.HERE,
                            page=i,
                        ).pack(),
                    )
                )
            else:
                page_buttons.append(
                    InlineKeyboardButton(
                        text=f"{str(i)}",
                        callback_data=PaginationCB(
                            action=PaginationActions.JUMP,
                            page=i,
                        ).pack(),
                    )
                )

        return InlineKeyboardMarkup(
            inline_keyboard=[*ads_buttons, page_buttons, add_button, back_buttons]
        )


async def ads_pagination(page: int = 1, page_size: int = 5) -> InlineKeyboardMarkup:
    offset = (page - 1) * page_size
    query: QuerySet = AdsModel.all().offset(offset).limit(page_size)
    ads = await query
    page_count = await AdsModel.all()
    page_count = len(page_count) / page_size
    if page_count > int(page_count):
        page_count = int(page_count) + 1
    else:
        page_count = int(page_count)

    keyboard = await generate_ads_keyboard(ads, page, page_count)
    return keyboard
