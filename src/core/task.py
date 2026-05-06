from pydantic import BaseModel, Field
from typing import List, Optional
import json
from pathlib import Path

class BatchTask(BaseModel):
    """
    批处理任务项
    """
    name: str = Field(..., description="任务名称")
    git_url: Optional[str] = Field(None, description="Git 仓库链接")
    local_dir: str = Field(..., description="本地工作目录")
    commands: List[str] = Field(..., description="要执行的命令行指令列表")
    branch: str = Field("main", description="Git 分支")

class BatchConfig(BaseModel):
    """
    批处理配置
    """
    tasks: List[BatchTask]

    @classmethod
    def from_file(cls, file_path: str | Path) -> "BatchConfig":
        """从 JSON 文件加载配置"""
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls(**data)
