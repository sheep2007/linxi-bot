from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message, GroupMessageEvent
from nonebot.permission import SUPERUSER
from nonebot.plugin import PluginMetadata
from nonebot.params import CommandArg
from nonebot.log import logger
from linxi.utils.utils import is_number, get_message_img
from linxi.utils.message_builder import image
from linxi.utils.message_builder import text as _text
from linxi.utils.message_builder import at


__usage__ = """
群员指令：
    /对话超管 <内容>

超管指令：
    /t: 查看当前存储的消息
    /t [qq] [group] [文本]: 在group回复指定用户
    /t [qq] [文本]: 私聊用户
    /t -1 [group] [文本]: 在group内发送消息
    /t [id] [文本]: 回复指定id的对话，id在 /t 中获取
"""

__plugin_meta__ = PluginMetadata(
    name="对话超管",
    description=f"跨越时空与管理员对话",
    usage=__usage__,
    extra={"unique_name": "dialogue", "example": "/对话超管 我喜欢你"},
)


dialogue_data = {}


dialogue = on_command("联系超管", aliases={"联系管理", "对话超管"}, priority=5, block=True)
reply = on_command("t", priority=1, permission=SUPERUSER, block=True)


@dialogue.handle()
async def _(bot: Bot, event: MessageEvent, arg: Message = CommandArg()):
    text = arg.extract_plain_text().strip()
    img_msg = _text("")
    for img in get_message_img(event.json()):
        img_msg += image(img)
    if not text and not img_msg:
        await dialogue.send("请发送联系管理+您要说的内容~", at_sender=True)
    else:
        group_id = 0
        group_name = "None"
        nickname = event.sender.nickname
        if isinstance(event, GroupMessageEvent):
            group_id = event.group_id
            group_name = (await bot.get_group_info(group_id=event.group_id))[
                "group_name"
            ]
            nickname = event.sender.card or event.sender.nickname
        for coffee in bot.config.superusers:
            await bot.send_private_msg(
                user_id=int(coffee),
                message=_text(
                    f"*****一份交流报告*****\n"
                    f"昵称：{nickname}({event.user_id})\n"
                    f"群聊：{group_name}({group_id})\n"
                    f"消息：{text}"
                )
                + img_msg,
            )
        await dialogue.send(
            _text(f"您的话已发送至管理员！\n======\n{text}") + img_msg, at_sender=True
        )
        nickname = event.sender.nickname if event.sender.nickname else event.sender.card
        dialogue_data[len(dialogue_data)] = {
            "nickname": nickname,
            "user_id": event.user_id,
            "group_id": group_id,
            "group_name": group_name,
            "msg": _text(text) + img_msg,
        }
        # print(dialogue_data)
        logger.info(f"Q{event.user_id}@群{group_id} 联系管理员：text:{text}")


@reply.handle()
async def _(bot: Bot, event: MessageEvent, arg: Message = CommandArg()):
    msg = arg.extract_plain_text().strip()
    if not msg:
        result = "*****待回复消息总览*****\n"
        for key in dialogue_data.keys():
            result += (
                f"id：{key}\n"
                f'\t昵称：{dialogue_data[key]["nickname"]}({dialogue_data[key]["user_id"]})\n'
                f'\t群群：{dialogue_data[key]["group_name"]}({dialogue_data[key]["group_id"]})\n'
                f'\t消息：{dialogue_data[key]["msg"]}'
                f"\n--------------------\n"
            )
        await reply.finish(Message(result[:-1]))
    msg = msg.split()
    text = ""
    group_id = 0
    user_id = -1
    if is_number(msg[0]):
        if len(msg[0]) < 3:
            msg[0] = int(msg[0])
            if msg[0] >= 0:
                id_ = msg[0]
                user_id = dialogue_data[id_]["user_id"]
                group_id = dialogue_data[id_]["group_id"]
                text = " ".join(msg[1:])
                dialogue_data.pop(id_)
            else:
                user_id = 0
                if is_number(msg[1]):
                    group_id = int(msg[1])
                    text = " ".join(msg[2:])
                else:
                    await reply.finish("群号错误...", at_sender=True)
        else:
            user_id = int(msg[0])
            if is_number(msg[1]) and len(msg[1]) > 5:
                group_id = int(msg[1])
                text = " ".join(msg[2:])
            else:
                group_id = 0
                text = " ".join(msg[1:])
    else:
        await reply.finish("第一参数，请输入数字.....", at_sender=True)
    for img in get_message_img(event.json()):
        text += image(img)
    if group_id:
        if user_id:
            await bot.send_group_msg(
                group_id=group_id, message=at(user_id) + "\n管理员回复\n=======\n" + text
            )
        else:
            await bot.send_group_msg(group_id=group_id, message=text)
        await reply.finish("消息发送成功...", at_sender=True)
    else:
        if user_id in [qq["user_id"] for qq in await bot.get_friend_list()]:
            await bot.send_private_msg(
                user_id=user_id, message="管理员回复\n=======\n" + text
            )
            await reply.finish("发送成功", at_sender=True)
        else:
            await reply.send(
                f"对象不是{list(bot.config.nickname)[0]}的好友...", at_sender=True
            )
