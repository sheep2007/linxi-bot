from typing import List

from linxi.configs.config import Config
from nonebot import on_command
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message
from nonebot.adapters.onebot.v11.permission import GROUP
from nonebot.params import CommandArg
from nonebot.plugin import PluginMetadata
from nonebot.log import logger
from linxi.utils.depends import ImageList
from linxi.utils.message_builder import image
from linxi.configs.path_config import DATA_PATH

from ._data_source import custom_group_welcome

try:
    import ujson as json
except ModuleNotFoundError:
    import json

__plugin_usage__ = """
usage：
    指令：
        设置：.设置入群欢迎 [文本] [图片] [at]
        查看：.查看入群欢迎
        Tips：可以通过 [at] 来确认是否艾特新成员
""".strip()


__plugin_meta__ = PluginMetadata(
    name="入群欢迎",
    description="为每个群设置不同的入群欢迎",
    usage=__plugin_usage__,
    extra={
        "unique_name": "welcome",
        "example": "/设置入群欢迎 欢迎你[at]"
    }
)


custom_welcome = on_command(
    "设置入群欢迎",
    aliases={"自定义欢迎消息", "自定义群欢迎消息", "设置群欢迎消息"},
    permission=GROUP,
    priority=5,
    block=True,
)


@custom_welcome.handle()
async def _(
    event: GroupMessageEvent, arg: Message = CommandArg(), img: List[str] = ImageList()
):
    msg = arg.extract_plain_text().strip()
    if not msg and not img:
        await custom_welcome.finish(__plugin_usage__)
    try:
        await custom_welcome.send(
            await custom_group_welcome(msg, img, event.user_id, event.group_id),
            at_sender=True,
        )
        logger.info(
            f"USER {event.user_id} GROUP {event.group_id} 自定义群欢迎消息：{msg}")
    except Exception as e:
        logger.error(f"自定义进群欢迎消息发生错误 {type(e)}：{e}")
        await custom_welcome.send("发生了一些未知错误...")


view_custom_welcome = on_command(
    "群欢迎消息", aliases={"查看入群欢迎", "入群欢迎"}, permission=GROUP, priority=5, block=True
)


@view_custom_welcome.handle()
async def _(event: GroupMessageEvent):
    img = ""
    msg = ""
    if (DATA_PATH / "custom_welcome_msg" / f"{event.group_id}.jpg").exists():
        img = image(DATA_PATH / "custom_welcome_msg" / f"{event.group_id}.jpg")
    custom_welcome_msg_json = (
        DATA_PATH / "custom_welcome_msg" / "custom_welcome_msg.json"
    )
    if custom_welcome_msg_json.exists():
        data = json.load(open(custom_welcome_msg_json, "r"))
        if data.get(str(event.group_id)):
            msg = data[str(event.group_id)]
            if msg.find("[at]") != -1:
                msg = msg.replace("[at]", "")
    if img or msg:
        await view_custom_welcome.finish(msg + img, at_sender=True)
    else:
        await view_custom_welcome.finish("当前还没有自定义群欢迎消息哦", at_sender=True)
