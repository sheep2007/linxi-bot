import re
from typing import Union
from nonebot import on_message
from nonebot.plugin import PluginMetadata
from nonebot.adapters.onebot.v11 import MessageEvent, Message

# 适配频道，不需要可自行注释
from nonebot_plugin_guild_patch import Message, GuildMessageEvent

from .data_source import get_github_reposity_information


__plugin_meta__ = PluginMetadata(
    name="Github",
    description=f"Github链接解析",
    usage="当Bot接收到一个 Github 仓库链接时，会自动发送信息卡片",
    extra={
        "unique_name": "github",
        "auther": "mute. <mute231010@gmail.com>",
        "version": "0.0.1",
    },
)


github = on_message(priority=99)


@github.handle()
async def github_handle(event: Union[MessageEvent, GuildMessageEvent]):
    url = event.get_plaintext()
    if re.match("https://github.com/.*?/.*?", url) != None:
        imageUrl = await get_github_reposity_information(url)
        if imageUrl != "获取信息失败":
            await github.finish(
                Message(
                    f"[CQ:image,file=https://image.thum.io/get/width/1280/crop/1440/viewportWidth/1280/png/noanimate/{url}]"
                )
            )
        else:
            await github.finish(Message(f"[CQ:image,file={imageUrl}]"))
