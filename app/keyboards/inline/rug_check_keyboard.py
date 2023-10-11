from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def get_link_keyboard(data) -> InlineKeyboardMarkup:
    buttons = []
    lstbtn = []
    for i in range(len(data)):
        lstbtn.append(
            InlineKeyboardButton(
                text=data[i]["name"], url=data[i]["url"]
            )
        )
        if i % 2 == 0:
            buttons.append(lstbtn)
            lstbtn = []
        elif i == len(data) - 1:
            buttons.append(lstbtn)
    return InlineKeyboardMarkup(inline_keyboard=[*buttons])
