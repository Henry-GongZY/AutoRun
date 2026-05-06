from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseValidator(ABC):
    """
    校验规则抽象基类
    """
    @abstractmethod
    def validate(self, data: Any) -> bool:
        """
        执行校验逻辑
        :param data: 需要校验的数据
        :return: 校验是否通过
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """校验规则名称"""
        pass

    @property
    def error_message(self) -> str:
        """默认错误信息"""
        return f"Validation failed for {self.name}"
