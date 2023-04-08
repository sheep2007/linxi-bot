import nonebot
from nonebot import logger
from nonebot.adapters.onebot.v11 import (
    Bot,
    ActionFailed,
    GroupMessageEvent,
    GroupRequestEvent,
    Event,
    HonorNotifyEvent,
    GroupUploadNoticeEvent,
    GroupDecreaseNoticeEvent,
    GroupIncreaseNoticeEvent,
    GroupAdminNoticeEvent,
    LuckyKingNotifyEvent,
    GroupRecallNoticeEvent,
)
from nonebot.matcher import Matcher
from nonebot.message import run_preprocessor, IgnoredException
from nonebot.typing import T_State

# from .switcher import switcher_integrity_check
from .config import plugin_config, global_config
from .path import *
from .utils import json_load

cb_notice = plugin_config.callback_notice
su = global_config.superusers
admin_path = Path(__file__).parts[-2]


@run_preprocessor
async def _(matcher: Matcher, bot: Bot, state: T_State, event: Event):
    module = str(matcher.module_name).split(".")
    if len(module) < 2 or module[-2] != admin_path:
        return  # 位置与文件路径有关
    which_module = module[-1]
    # logger.info(f"{which_module}插件开始hook处理")
    if isinstance(
        event,
        (
            GroupMessageEvent,
            HonorNotifyEvent,
            GroupUploadNoticeEvent,
            GroupDecreaseNoticeEvent,
            GroupIncreaseNoticeEvent,
            GroupAdminNoticeEvent,
            LuckyKingNotifyEvent,
            GroupRecallNoticeEvent,
        ),
    ):
        gid = event.group_id

    elif isinstance(event, GroupRequestEvent):
        gid = event.group_id
        try:
            if which_module == "requests":
                logger.info(event.flag)
                if event.sub_type == "add":
                    re_msg = (
                        f"群{gid}收到{event.user_id}的加群请求，flag为：{event.flag}\n发送【.请求同意/拒绝】"
                    )
                    logger.info(re_msg)
                    if cb_notice:
                        try:
                            for qq in su:
                                await bot.send_msg(user_id=qq, message=re_msg)
                        except ActionFailed:
                            logger.info("发送消息失败,可能superuser之一不是好友")
                else:
                    pass
        except ActionFailed:
            pass
        except FileNotFoundError:
            pass
