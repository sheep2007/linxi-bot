from typing import Set

from pydantic import BaseModel, Field, Extra


class Config(BaseModel, extra=Extra.ignore):
    b23_commands: Set[str] = Field(default={"bili 热搜", "bili hot", "B站热搜"})
    b23_block: bool = Field(default=False)
    b23_priority: int = Field(default=99)
