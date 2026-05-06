import logging
import os
import subprocess
from typing import List, Set
from .task import BatchTask
from ..utils.git_helper import GitHelper

logger = logging.getLogger(__name__)

class TaskRunner:
    # 记录正在同步的任务路径，防止并发冲突
    syncing_paths: Set[str] = set()

    def __init__(self, tasks: List[BatchTask]):
        self.tasks = tasks

    def run_all(self):
        """执行所有任务"""
        for task in self.tasks:
            self.run_task(task)

    def is_syncing(self, path: str) -> bool:
        """检查某个路径是否正在同步"""
        return path in self.syncing_paths

    def run_task(self, task: BatchTask):
        """执行单个任务"""
        if self.is_syncing(task.local_dir):
            logger.warning(f"Task {task.name} is currently syncing. Execution skipped.")
            raise RuntimeError(f"项目 {task.name} 正在同步中，请稍后再试。")

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
