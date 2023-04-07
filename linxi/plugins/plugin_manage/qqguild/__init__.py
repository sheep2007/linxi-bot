from argparse import Namespace

from nonebot.matcher import Matcher
from nonebot.params import ShellCommandArgs
from nonebot.message import run_preprocessor
from nonebot.exception import IgnoredException
from nonebot.plugin import on_shell_command, get_loaded_plugins
from nonebot_plugin_guild_patch import Bot, GuildMessageEvent

from .handle import Handle
from .parser import npm_parser
from .manager import plugin_manager

npm = on_shell_command("plugin", parser=npm_parser, priority=1)

# 在 Matcher 运行前检测其是否启用
@run_preprocessor
async def _(matcher: Matcher, bot: Bot, event: GuildMessageEvent):
    plugin = matcher.plugin_name

    conv = {
        "user": [event.user_id] if hasattr(event, "user_id") else [],  # type: ignore
        "channel": [event.channel_id] if hasattr(event, "channel_id") else [],  # type: ignore
    }

    if (
        hasattr(event, "user_id")
        and not hasattr(event, "channel_id")
        and str(event.user_id) in bot.config.guild_superusers  # type: ignore
    ):
        conv["user"] = []
        conv["channel"] = []

    plugin_manager.update_plugin(
        {
            str(p.name): p.name != "plugin_manage" and bool(p.matcher)
            for p in get_loaded_plugins()
        }
    )

    if plugin and not plugin_manager.get_plugin(conv=conv, perm=1)[plugin]:
        raise IgnoredException(f"Linxi Plugin Manager has blocked {plugin} !")


@npm.handle()
async def _(bot: Bot, event: GuildMessageEvent, args: Namespace = ShellCommandArgs()):
    args.conv = {
        "user": [event.user_id],
        "channel": [event.channel_id] if isinstance(event, GuildMessageEvent) else [],
    }
    args.is_admin = (
        event.sender.role in ["admin", "owner"]
        if isinstance(event, GuildMessageEvent)
        else False
    )
    args.is_superuser = str(event.user_id) in bot.config.guild_superusers

    if hasattr(args, "handle"):
        message = getattr(Handle, args.handle)(args)
        if message is not None:
            message = message.split("\n")
            if len(message) > 15:
                i = 1
                messages = []
                while len(message) > 15:
                    messages.append("\n".join(message[:15]) + f"\n【第{i}页】")
                    message = message[15:]
                    i = i + 1
                messages.append("\n".join(message[:15]) + f"\n【第{i}页-完】")
                bot.send(messages)
            else:
                await bot.send(event, "\n".join(message[:30]))
