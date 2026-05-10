from .jdd_validator import JDDValidator
from .hdr_validator import HDRValidator
from .ce_validator import CEValidator
from typing import Any
import logging

GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

logger = logging.getLogger(__name__)

def run_all_validators(data: Any):
    """
    按顺序执行校验器，模拟单元测试输出效果
    """
    validators = [
        JDDValidator(),
        HDRValidator(),
        CEValidator()
    ]

    print("\n" + "="*40)
    print("RUNNING VALIDATORS".center(40))
    print("="*40)

    results = []
    failed_any = False

    for validator in validators:
        label = f"{validator.name:.<30}"
        try:
            passed = validator.validate(data)
            if passed:
                print(f"{label} {GREEN}[ PASS ]{RESET}")
                results.append(True)
            else:
                print(f"{label} {RED}[ FAIL ]{RESET}")
                logger.error(f"Validation Error: {validator.error_message}")
                results.append(False)
                failed_any = True
        except Exception as e:
            print(f"{label} {RED}[ ERROR ]{RESET}")
            logger.error(f"System Error in {validator.name}: {str(e)}")
            results.append(False)
            failed_any = True

    print("-" * 40)
    passed_count = results.count(True)
    failed_count = results.count(False)
    
    summary = f"Summary: {passed_count} passed, {failed_count} failed"
    if failed_any:
        print(f"{RED}{summary}{RESET}")
        print("="*40 + "\n")
        raise ValueError(f"校验未通过: {passed_count} 成功, {failed_count} 失败")
    else:
        print(f"{GREEN}{summary}{RESET}")
        print("="*40 + "\n")
