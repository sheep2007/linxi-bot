# python3
# -*- coding: utf-8 -*-
# @Time    : 2021/12/23 0:52
# @Author  : yzyyz
# @Email   :  youzyyz1384@qq.com
# @File    : __init__.py.py
# @Software: PyCharm

import nonebot
from nonebot.plugin import PluginMetadata

from . import (
    admin,
    approve,
    auto_ban,
    auto_ban_,
    func_hook,
    group_request_verify,
    notice,
    particular_e_notice,
    requests,
    request_manual,
    utils
)
from .config import global_config
from .path import *
from .utils import At, Reply, MsgText, banSb, change_s_title, log_sd, fi, log_fi, sd, init

from . import blacklist
from . import welcome

su = global_config.superusers
driver = nonebot.get_driver()


@driver.on_bot_connect
async def _():
    await init() 


"""
! 消息防撤回模块，默认不开启，有需要的自行开启，想对部分群生效也需自行实现(可以并入本插件的开关系统内，也可控制 go-cqhttp 的事件过滤器)

如果在 go-cqhttp 开启了事件过滤器，请确保允许 post_type = notice 通行
【至少也得允许 notice_type = group_recall 通行】
"""

__usage__ = """
【群管】：
权限：permission = SUPERUSER | GROUP_ADMIN | GROUP_OWNER
  禁言:
    禁 @某人 时间（s）[1,2591999]
    禁 时间（s）@某人 [1,2591999]
    禁 @某人 缺省时间则随机
    禁 @某人 0 可解禁
    解 @某人
  全群禁言
    全员禁言 
    全员禁言 解
  踢出：
    踢 @某人
  踢出并拉黑：
   黑 @某人
  设置精华（回复该消息）
    设精
  取消精华（回复该消息）
    取消精华

【加群自动审批】：
群内发送 permission = GROUP_ADMIN | GROUP_OWNER | SUPERUSER
  查看词条 ： 查看本群审批词条   或/审批
  词条+ [词条] ：增加审批词条 或/审批+
  词条- [词条] ：删除审批词条 或/审批-

【Bot 管理员】：
  所有词条 ：  查看所有审批词条   或/su审批
  指定词条+ [群号] [词条] ：增加指定群审批词条 或/su审批+
  指定词条- [群号] [词条] ：删除指定群审批词条 或/su审批-
  自动审批处理结果将发送给superuser

【分群管理员设置】*分管：可以接受加群处理结果消息的用户
群内发送 permission = GROUP_ADMIN | GROUP_OWNER | SUPERUSER
  分管+ [user] ：user可用@或qq 添加分群管理员
  分管- [user] ：删除分群管理员
  查看分管 ：查看本群分群管理员

群内或私聊 permission = SUPERUSER
  所有分管 ：查看所有分群管理员
  群管接收 ：打开或关闭超管消息接收（关闭则审批结果不会发送给superusers）

【入群欢迎】
  设置入群欢迎 [文本] [图片] [at]
  查看入群欢迎
  Tips：可以通过 [at] 来确认是否艾特新成员

"""
__help_plugin_name__ = '简易群管'

__plugin_meta__ = PluginMetadata(
    name="群管",
    description="群管理",
    usage=__usage__,
    extra={
        "unique_name": "manage",
        "example": "无"
    }
)