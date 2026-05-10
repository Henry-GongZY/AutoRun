from pydantic import BaseModel, Field
from typing import List, Optional

class BatchTask(BaseModel):
    """
    批处理任务项
    """
    name: str = Field(..., description="任务名称")
    git_url: Optional[str] = Field(None, description="Git 仓库链接")
    local_dir: str = Field(..., description="本地工作目录")
    commands: List[str] = Field(..., description="要执行的命令行指令列表")
    branch: str = Field("main", description="Git 分支")
