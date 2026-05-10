from .base import BaseValidator
from typing import Any

class JDDValidator(BaseValidator):
    """
    示例校验：检查项目名称是否符合规范
    """
    def __init__(self, prefix: str = "AUTO-"):
        self.prefix = prefix

    @property
    def name(self) -> str:
        return "ProjectNameValidator"

    def validate(self, data: Any) -> bool:
        if isinstance(data, str) and data.startswith(self.prefix):
            return True
        return False

    @property
    def error_message(self) -> str:
        return f"项目名称必须以 '{self.prefix}' 开头"
