from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot_plugin_guild_patch import GuildMessageEvent
from ..matcher import arc


async def default_handler(event: MessageEvent | GuildMessageEvent):
    await arc.finish(MessageSegment.reply(event.message_id) + "不支持的命令参数")
