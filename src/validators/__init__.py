from .jdd_validator import JDDValidator
from .hdr_validator import HDRValidator
from .ce_validator import CEValidator
from typing import Any
import logging

logger = logging.getLogger(__name__)

def run_all_validators(data: Any):
    """
    按顺序执行校验器：JDD -> HDR -> CE
    """
    validators = [
        JDDValidator(),
        HDRValidator(),
        CEValidator()
    ]

    for validator in validators:
        logger.info(f"Running validator: {validator.name}")
        if not validator.validate(data):
            error_msg = f"校验失败 [{validator.name}]: {validator.error_message}"
            logger.error(error_msg)
            raise ValueError(error_msg)
    
    logger.info("所有校验规则通过！")
