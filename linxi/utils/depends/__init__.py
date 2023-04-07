from typing import Callable, List, Optional, Tuple, Union

from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageEvent
from nonebot.internal.matcher import Matcher
from nonebot.internal.params import Depends


# from models.user_shop_gold_log import UserShopGoldLog
from linxi.utils.utils import (
    get_message_at,
    get_message_img,
)


async def _match(
    matcher: Matcher,
    event: MessageEvent,
    msg: Optional[str],
    func: Callable,
    contain_reply: bool,
):
    _list = func(event.message)
    if event.reply and contain_reply:
        _list = func(event.reply.message)
    if not _list and msg:
        await matcher.finish(msg)
    return _list


def ImageList(msg: Optional[str] = None, contain_reply: bool = True) -> List[str]:
    """
    说明:
        获取图片列表（包括回复时），含有msg时不能为空，为空时提示并结束事件
    参数:
        :param msg: 提示文本
        :param contain_reply: 包含回复内容
    """

    async def dependency(matcher: Matcher, event: MessageEvent):
        return await _match(matcher, event, msg, get_message_img, contain_reply)

    return Depends(dependency)



def AtList(msg: Optional[str] = None, contain_reply: bool = True) -> List[int]:
    """
    说明:
        获取at列表（包括回复时），含有msg时不能为空，为空时提示并结束事件
    参数:
        :param msg: 提示文本
        :param contain_reply: 包含回复内容
    """

    async def dependency(matcher: Matcher, event: MessageEvent):
        return [
            int(x)
            for x in await _match(matcher, event, msg, get_message_at, contain_reply)
        ]

    return Depends(dependency)