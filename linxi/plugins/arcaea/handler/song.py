from nonebot.adapters.onebot.v11 import MessageEvent, Message, MessageSegment
from nonebot_plugin_guild_patch import Message, GuildMessageEvent
from nonebot.params import CommandArg
from ..matcher import arc
from ..message.text_message import TextMessage
from ..api.request import API
from ..schema import diffstr2num


async def song_handler(
    event: MessageEvent | GuildMessageEvent, arg: Message = CommandArg()
):
    """
    /arc song Fracture Ray ftr
    """
    args = arg.extract_plain_text().split()
    if len(args) >= 2 and args[0] == "song":
        # get args
        difficulty = diffstr2num(args[-1].upper())
        if difficulty is not None:
            songname = " ".join(args[1:-1])
        else:
            difficulty = -1
            songname = " ".join(args[1:])
        # query
        resp = await API.get_song_info(songname=songname)
        if error_message := resp.message:
            await arc.finish(MessageSegment.reply(event.message_id) + error_message)
        await arc.finish(
            MessageSegment.reply(event.message_id)
            + TextMessage.song_info(data=resp, difficulty=difficulty)
        )
