from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent
from nonebot.typing import T_State
from nonebot.plugin import PluginMetadata

from linxi.configs.config import NICKNAME

__plugin_meta__ = PluginMetadata(
    name="消息撤回",
    description=f"撤回用户消息，需要 {NICKNAME} 拥有管理员权限",
    usage="回复需要撤回的消息并发送 /撤回",
    extra={"unique_name": "withdraw", "example": "暂无"},
)


withdraw_msg = on_command("撤回", priority=5, block=True)


@withdraw_msg.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    if event.reply:
        await bot.delete_msg(message_id=event.reply.message_id)
