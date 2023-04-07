from nonebot.plugin import PluginMetadata

from .group import *
from .qqguild import *

__plugin_meta__ = PluginMetadata(
    name="插件管理器",
    description="管理群聊插件",
    usage="""
    插件管理器

    获取功能列表：/plugin ls
    关闭功能：/plugin block <功能名>
    开启功能：/plugin unblock <功能名>

    更多参数请看文档
    """,
)
