import subprocess
import os
import logging
from typing import List
from .task import BatchTask
from ..utils.git_helper import GitHelper

logger = logging.getLogger(__name__)

class TaskRunner:
    def __init__(self, tasks: List[BatchTask]):
        self.tasks = tasks

    def run_all(self):
        """执行所有任务"""
        for task in self.tasks:
            self.run_task(task)

    def run_task(self, task: BatchTask):
        """执行单个任务"""
        logger.info(f"--- Starting Task: {task.name} ---")
        
        # 1. 处理 Git 同步
        if task.git_url:
            success = GitHelper.ensure_repo(task.local_dir, task.git_url, task.branch)
            if not success:
                logger.error(f"Task {task.name} aborted due to git sync failure.")
                return

        # 2. 检查目录
        if not os.path.exists(task.local_dir):
            logger.error(f"Directory {task.local_dir} not found. Skipping commands.")
            return

        # 3. 执行命令
        for cmd in task.commands:
            logger.info(f"Executing command: {cmd} (in {task.local_dir})")
            try:
                # 使用 shell=True 允许执行复杂的 shell 命令，但要注意安全
                subprocess.run(cmd, shell=True, cwd=task.local_dir, check=True)
            except subprocess.CalledProcessError as e:
                logger.error(f"Command failed: {cmd}. Error: {e}")
                break  # 如果其中一个命令失败，跳过该任务后续命令
        
        logger.info(f"--- Task {task.name} Finished ---")
