import asyncio
import os
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import List

import ujson as json
from nonebot.adapters.onebot.v11.message import MessageSegment

from linxi.configs.config import Config
from linxi.configs.path_config import DATA_PATH, IMAGE_PATH
from nonebot.log import logger
from linxi.utils.http_utils import AsyncHttpx

from linxi.utils.message_builder import image

custom_welcome_msg_json = (
    Path() / "data" / "custom_welcome_msg" / "custom_welcome_msg.json"
)

ICON_PATH = IMAGE_PATH / "other"


async def custom_group_welcome(
    msg: str, img_list: List[str], user_id: int, group_id: int
) -> str:
    """
    说明:
        替换群欢迎消息
    参数:
        :param msg: 欢迎消息文本
        :param img_list: 欢迎消息图片，只取第一张
        :param user_id: 用户id，用于log记录
        :param group_id: 群号
    """
    img_result = ""
    result = ""
    img = img_list[0] if img_list else ""
    if (DATA_PATH / f"custom_welcome_msg/{group_id}.jpg").exists():
        (DATA_PATH / f"custom_welcome_msg/{group_id}.jpg").unlink()
    data = {}
    if not custom_welcome_msg_json.exists():
        custom_welcome_msg_json.parent.mkdir(parents=True, exist_ok=True)
    else:
        try:
            data = json.load(open(custom_welcome_msg_json, "r"))
        except FileNotFoundError:
            pass
    try:
        if msg:
            data[str(group_id)] = str(msg)
            json.dump(
                data, open(custom_welcome_msg_json, "w"), indent=4, ensure_ascii=False
            )
            logger.info(f"USER {user_id} GROUP {group_id} 更换群欢迎消息 {msg}")
            result += msg
        if img:
            await AsyncHttpx.download_file(
                img, DATA_PATH / "custom_welcome_msg" / f"{group_id}.jpg"
            )
            img_result = image(DATA_PATH / "custom_welcome_msg" / f"{group_id}.jpg")
            logger.info(f"USER {user_id} GROUP {group_id} 更换群欢迎消息图片")
    except Exception as e:
        logger.error(f"GROUP {group_id} 替换群消息失败 e:{e}")
        return "替换群消息失败.."
    return f"替换群欢迎消息成功：\n{result}" + img_result
