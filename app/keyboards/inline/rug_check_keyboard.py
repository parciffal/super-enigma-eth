from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def get_link_keyboard(data: dict) -> InlineKeyboardMarkup:
    buttons = []
    lstbtn = []
    for i in range(len(data["links"])):
        if i % 2 == 0:
            buttons.append(lstbtn)
            lstbtn = []
        elif i == len(data["links"]) - 1:
            buttons.append(lstbtn)
        lstbtn.append(
            InlineKeyboardButton(
                text=data["links"][i]["name"], url=data["links"][i]["url"]
            )
        )
    return InlineKeyboardMarkup(inline_keyboard=[*buttons])
