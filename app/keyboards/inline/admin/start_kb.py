from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def first_start_keyboard(username: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Add to Group",
                                 url=f"https://telegram.me/{username}?startgroup=true")
        ]
    ])