from ..matcher import arc
from ..assets_updater import AssetsUpdater
from ..resource_manager import db_root as ROOT
from nonebot.adapters.onebot.v11 import Message, MessageEvent, MessageSegment
from nonebot_plugin_guild_patch import GuildMessageEvent

from nonebot.params import CommandArg
from os import path
from shutil import rmtree
from typing import List, Union


async def assets_update_handler(event: Union[MessageEvent, GuildMessageEvent], arg: Message = CommandArg()):
    args: List = arg.extract_plain_text().split()
    if args[0] == "assets_update":
        if len(args) == 2:
            if args[1] == "-purge":
                rmtree(ROOT / "assets", ignore_errors=True)
        await arc.send("正在更新，请关注控制台更新进度…")

        result_song = await AssetsUpdater.check_song_update()
        result_char = await AssetsUpdater.check_char_update()

        await arc.finish(
            MessageSegment.reply(event.message_id)
            + "\n".join(
                [
                    f"成功更新 {len(result_song)} 张曲绘, ",
                    f"成功更新 {len(result_char)} 张立绘",
                ]
            )
        )
