# python3
# -*- coding: utf-8 -*-
# @Time    : 2022/12/19 3:01
# @Author  : yzyyz
# @Email   :  youzyyz1384@qq.com
# @File    : admin.py
# @Software: PyCharm
import asyncio
from random import randint
from traceback import print_exc

from nonebot import on_command, logger
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent
from nonebot.adapters.onebot.v11.exception import ActionFailed
from nonebot.adapters.onebot.v11.permission import GROUP_ADMIN, GROUP_OWNER
from nonebot.matcher import Matcher
from nonebot.permission import SUPERUSER
from .admin_role import DEPUTY_ADMIN

from .config import global_config
from .utils import At, MsgText, banSb, change_s_title, fi, log_fi, sd, Reply, log_sd

su = global_config.superusers

ban = on_command(
    "禁",
    aliases={"ban"},
    priority=1,
    block=True,
    permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER | DEPUTY_ADMIN,
)


@ban.handle()
async def _(bot: Bot, matcher: Matcher, event: GroupMessageEvent):
    """
    /禁 @user 禁言
    """
    try:
        msg = MsgText(event.json()).replace(" ", "").replace("禁", "")
        time = int(
            "".join(
                map(
                    str, list(map(lambda x: int(x), filter(lambda x: x.isdigit(), msg)))
                )
            )
        )
        # 提取消息中所有数字作为禁言时间
    except ValueError:
        time = None
    sb = At(event.json())
    gid = event.group_id
    if sb:
        baning = banSb(gid, ban_list=sb, time=time)
        try:
            async for baned in baning:
                if baned:
                    await baned
            await log_fi(matcher, "禁言操作成功" if time is not None else "用户已被禁言随机时长")
        except ActionFailed:
            await fi(matcher, "权限不足")


unban = on_command(
    "解",
    aliases={"unban"},
    priority=1,
    block=True,
    permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER | DEPUTY_ADMIN,
)


@unban.handle()
async def _(bot: Bot, matcher: Matcher, event: GroupMessageEvent):
    """
    /解 @user 解禁
    """
    sb = At(event.json())
    gid = event.group_id
    if sb:
        baning = banSb(gid, ban_list=sb, time=0)
        try:
            async for baned in baning:
                if baned:
                    await baned
            await log_fi(matcher, "解禁操作成功")
        except ActionFailed:
            await fi(matcher, "权限不足")


ban_all = on_command(
    "ban all",
    aliases={"全体禁言", "全禁", "全员禁言"},
    permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER | DEPUTY_ADMIN,
    priority=1,
    block=True,
)


@ban_all.handle()
async def _(bot: Bot, matcher: Matcher, event: GroupMessageEvent):
    """
    # note: 如果在 .env.* 文件内设置了 COMMAND_START ，且不包含 "" (即所有指令都有前缀，假设 '/' 是其中一个前缀)，则应该发 //all 触发
    /all 全员禁言
    /all  解 关闭全员禁言
    """
    msg = event.get_message()
    if msg and "解" in str(msg):
        enable = False
    else:
        enable = True
    try:
        await bot.set_group_whole_ban(group_id=event.group_id, enable=enable)
        await log_fi(matcher, f"全体操作成功: {'禁言' if enable else '解禁'}")
    except ActionFailed:
        await fi(matcher, "权限不足")


change = on_command(
    "改",
    aliases={"改昵称", "修改昵称"},
    permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER | DEPUTY_ADMIN,
    priority=1,
    block=True,
)


@change.handle()
async def _(bot: Bot, matcher: Matcher, event: GroupMessageEvent):
    """
    /改 @user xxx 改群昵称
    """
    msg = str(event.get_message())
    logger.info(msg.split())
    sb = At(event.json())
    gid = event.group_id
    if sb:
        try:
            for user_ in sb:
                await bot.set_group_card(
                    group_id=gid, user_id=int(user_), card=msg.split()[-1:][0]
                )
            await log_fi(matcher, "改名片操作成功")
        except ActionFailed:
            await fi(matcher, "权限不足")


kick = on_command(
    "踢",
    aliases={"kick"},
    permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER | DEPUTY_ADMIN,
    priority=1,
    block=True,
)


@kick.handle()
async def _(bot: Bot, matcher: Matcher, event: GroupMessageEvent):
    """
    /踢 @user 踢出某人
    """
    sb = At(event.json())
    gid = event.group_id
    if sb:
        if "all" not in sb:
            try:
                for qq in sb:
                    if qq == event.user_id:
                        await sd(matcher, "你在玩一种很新的东西，不能踢自己!")
                        continue
                    if qq in su or (str(qq) in su):
                        await sd(matcher, "超级用户不能被踢")
                        continue
                    await bot.set_group_kick(
                        group_id=gid, user_id=int(qq), reject_add_request=False
                    )
                await log_fi(matcher, "踢人操作执行完毕")
            except ActionFailed:
                await fi(matcher, "权限不足")
        await fi(matcher, "不能含有@全体成员")


kick_ = on_command(
    "黑",
    permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER | DEPUTY_ADMIN,
    priority=1,
    block=True,
)


@kick_.handle()
async def _(bot: Bot, matcher: Matcher, event: GroupMessageEvent):
    """
    黑 @user 踢出并拉黑某人
    """
    sb = At(event.json())
    gid = event.group_id
    if sb:
        if "all" not in sb:
            try:
                for qq in sb:
                    if qq == event.user_id:
                        await sd(matcher, "你在玩一种很新的东西，不能踢自己!")
                        continue
                    if qq in su or (str(qq) in su):
                        await sd(matcher, "超级用户不能被踢")
                        continue
                    await bot.set_group_kick(
                        group_id=gid, user_id=int(qq), reject_add_request=True
                    )
                await log_fi(matcher, "踢人并拉黑操作执行完毕")
            except ActionFailed:
                await fi(matcher, "权限不足")
        await fi(matcher, "不能含有@全体成员")


set_essence = on_command(
    "加精",
    aliases={"加精", "set_essence", "设精", "设为精华"},
    priority=5,
    block=True,
    permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER | DEPUTY_ADMIN,
)


@set_essence.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    rp = Reply(event.json())
    if rp:
        msg_id = rp["message_id"]
        await bot.call_api(api="set_essence_msg", message_id=msg_id)


del_essence = on_command(
    "取消精华",
    aliases={"取消加精", "del_essence"},
    priority=5,
    block=True,
    permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER | DEPUTY_ADMIN,
)


@del_essence.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    rp = Reply(event.json())
    if rp:
        msg_id = rp["message_id"]
        await bot.call_api(api="delete_essence_msg", message_id=msg_id)


exit = on_command(
    "退群", aliases={"exit"}, priority=5, block=True, permission=SUPERUSER | GROUP_OWNER
)


@exit.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    group_id: int = event.group_id
    await bot.set_group_leave(group_id, is_dismiss=False)
