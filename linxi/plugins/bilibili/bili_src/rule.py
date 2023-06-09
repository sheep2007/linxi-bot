from nonebot.adapters.onebot.v11 import Message, MessageSegment, MessageEvent, Event
from nonebot.adapters.onebot.v11.event import GroupMessageEvent, PrivateMessageEvent
from nonebot_plugin_guild_patch import GuildMessageEvent, Message, Event
from nonebot.log import logger

from nonebot.rule import Rule


async def isGroupMessage(event: Event) -> bool:
    if event.get_type() != "message":
        return False
    if not isinstance(event, GroupMessageEvent):
        return False
    return True


async def isPrivateMessage(event: Event) -> bool:
    if event.get_type() != "message":
        return False
    if not isinstance(event, PrivateMessageEvent):
        return False
    return True


async def isGuildMessage(event: Event) -> bool:
    if event.get_type() != "message":
        return False
    if not isinstance(event, GuildMessageEvent):
        return False
    return True


groupMessageRule = Rule(isGroupMessage)
privateMessageRule = Rule(isPrivateMessage)
guildMessageRule = Rule(isGuildMessage)
