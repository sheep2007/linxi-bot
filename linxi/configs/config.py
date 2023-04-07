import platform
from pathlib import Path
from typing import Optional

from .utils import ConfigsManager

if platform.system() == "Linux":
    import os

    hostip = (
        os.popen("cat /etc/resolv.conf | grep nameserver | awk '{ print $2 }'")
        .read()
        .replace("\n", "")
    )


# 回复消息名称
NICKNAME: str = "林汐"

SYSTEM_PROXY: Optional[str] = None  # 全局代理

Config = ConfigsManager(Path() / "data" / "configs" / "plugins2config.yaml")