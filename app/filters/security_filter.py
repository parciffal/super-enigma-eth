from typing import Callable, Union
from functools import wraps
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot


def security_decorator(group_id: Union[int, str]):
    """
    A security decorator for aiogram that checks
    if a user is a member of a specific group before executing a function.

    Args:
        group_id (Union[int, str]): The ID of the group to check membership against.

    Returns:
        Callable: A decorator that can be applied to functions
                  to enforce security based on group membership.

    """

    async def get_group_join_link(
        bot: Bot, group_id: int, *args, **kwargs
    ) -> Union[str, None]:
        """
        Get the join link for a group.

        Args:
            bot (Bot): The aiogram Bot instance.
            group_id (int): The ID of the group.

        Returns:
            Union[str, None]: The join link for the group, or None if unsuccessful.
        """
        try:
            chat_invite_link = await bot.export_chat_invite_link(chat_id=group_id)
            return chat_invite_link
        except Exception as e:
            print(f"Failed to get join link for group {group_id}: {e}")
            return None

    async def wrapped(message: Message, bot: Bot, *args, **kwargs) -> bool:
        """
        Check if the user associated with the given message
        is a member of the specified group.

        Args:
            message (Message): The message object.
            bot (Bot): The aiogram Bot instance.

        Returns:
            bool: True if the user is a member of the group, False otherwise.
        """
        user_id = message.from_user.id if message.from_user else message.chat.id
        chat_member = await bot.get_chat_member(chat_id=group_id, user_id=user_id)
        return chat_member.status in ["creator", "member", "administrator"]

    async def unauthorized(message: Message, bot: Bot, *args, **kwargs):
        """
        Send an unauthorized message to the user, prompting them to join the group.

        Args:
            message (Message): The message object.
            bot (Bot): The aiogram Bot instance.
        """
        link = await get_group_join_link(bot, group_id)
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="Join", url=link)]]
        )
        await message.answer(
            text="Please join our group before you can use the bot",
            reply_markup=keyboard,
        )

    def decorator(func: Callable) -> Callable:
        """
        Decorator to enforce security based on group membership.

        Args:
            func (Callable): The function to be decorated.

        Returns:
            Callable: The decorated function.
        """

        @wraps(func)
        async def decorated(*args, **kwargs):
            if group_id in ["", 0, None]:
                return await func(*args, **kwargs)
            elif await wrapped(*args, **kwargs):
                return await func(*args, **kwargs)
            else:
                return await unauthorized(*args, **kwargs)

        return decorated

    return decorator
