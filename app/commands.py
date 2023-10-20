from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeDefault

from app.config import Config

users_commands = {"start": "Get info about bot",
                  "help": "Get keyboard info ",
                  "autodetect": "On/Off autodetect",
                  "detect": "Send /detect address"}

# owner_commands = {**users_commands, "ping": "Check bot ping", "stats": "Show bot stats"}


async def setup_bot_commands(bot: Bot, config: Config):
    # await bot.set_my_commands(
    #     [
    #         BotCommand(command=command, description=description)
    #         for command, description in owner_commands.items()
    #     ],
    #     scope=BotCommandScopeChat(chat_id=config.settings.owner_id),
    # )

    await bot.set_my_commands(
        [
            BotCommand(command=command, description=description)
            for command, description in users_commands.items()
        ],
        scope=BotCommandScopeDefault(type="default"),
    )
    pass


async def remove_bot_commands(bot: Bot, config: Config):
    await bot.delete_my_commands(scope=BotCommandScopeDefault(type="default"))
    # await bot.delete_my_commands(
    #     scope=BotCommandScopeChat(chat_id=config.settings.owner_id)
    # )
    pass
