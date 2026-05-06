import sys
import logging
from src.config import settings
from src.clients.feishu_client import FeishuClient
from src.clients.gitlab_client import GitLabClient
from src.validators.example import ProjectNameValidator

# 配置日志
logging.basicConfig(level=settings.log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from src.core.task import BatchTask
from src.core.runner import TaskRunner

def main():
    logger.info("Initializing AutoRun project...")

    # 1. 客户端初始化示例
    feishu = FeishuClient(settings.feishu_app_id, settings.feishu_app_secret)
    gitlab = GitLabClient(settings.gitlab_url, settings.gitlab_private_token)

    # 2. 校验规则示例
    validator = ProjectNameValidator()
    test_name = "AUTO-MIGRATE"
    if validator.validate(test_name):
        logger.info(f"Validation passed for: {test_name}")

    # 3. 自动化批处理示例
    logger.info("--- Batch Processing Demo ---")
    
    # 定义一个任务（例如：拉取一个公开库并查看其内容）
    demo_task = BatchTask(
        name="Update Docs",
        git_url="https://github.com/larksuite/oapi-sdk-python.git", # 仅作示例
        local_dir="./temp_oapi_sdk",
        commands=[
            "ls -l",
            "echo 'Successfully synced and listed files'"
        ],
        branch="v2"
    )

    runner = TaskRunner(tasks=[demo_task])
    # 注意：在没有配置 Git 或网络环境的情况下，这里可能会失败
    # runner.run_all()
    logger.info("Task runner initialized. Uncomment 'runner.run_all()' in main.py to execute.")

if __name__ == "__main__":
    main()
