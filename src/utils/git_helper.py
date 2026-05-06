import os
import subprocess
import logging

logger = logging.getLogger(__name__)

class GitHelper:
    @staticmethod
    def ensure_repo(local_dir: str, git_url: str, branch: str = "main"):
        """
        确保本地仓库存在且为最新
        """
        if not os.path.exists(local_dir):
            logger.info(f"Directory {local_dir} does not exist. Cloning from {git_url}...")
            try:
                subprocess.run(["git", "clone", "-b", branch, git_url, local_dir], check=True)
                return True
            except subprocess.CalledProcessError as e:
                logger.error(f"Failed to clone repository: {e}")
                return False
        else:
            # 如果存在，尝试更新
            logger.info(f"Directory {local_dir} exists. Pulling latest changes...")
            try:
                subprocess.run(["git", "-C", local_dir, "pull", "origin", branch], check=True)
                return True
            except subprocess.CalledProcessError as e:
                logger.error(f"Failed to pull changes: {e}")
                return False

    @staticmethod
    def local_version(local_dir: str) -> str:
        """
        获取本地仓库的版本
        """
        try:
            # 获取短 hash 和提交信息
            result = subprocess.run(
                ["git", "-C", local_dir, "log", "-1", "--format=%h - %s"],
                capture_output=True, text=True, check=True
            )
            return result.stdout.strip()
        except Exception as e:
            logger.error(f"Failed to get local version: {e}")
            return ""

    @staticmethod
    def remote_version(local_dir: str, branch: str = "main") -> str:
        """
        获取远程仓库的版本
        """
        try:
            # 获取远程更新
            subprocess.run(["git", "-C", local_dir, "fetch"], check=True, capture_output=True)
            # 获取远程分支的最新 hash 和提交信息
            result = subprocess.run(
                ["git", "-C", local_dir, "log", "-1", f"origin/{branch}", "--format=%h - %s"],
                capture_output=True, text=True, check=True
            )
            return result.stdout.strip()
        except Exception as e:
            logger.error(f"Failed to get remote version: {e}")
            return ""

    @staticmethod
    def has_changes(local_dir: str, branch: str = "main") -> bool:
        """
        检查远程是否有更新（不拉取代码）
        """
        try:
            # 获取远程更新
            subprocess.run(["git", "-C", local_dir, "fetch"], check=True)
            # 比较本地与远程
            result = subprocess.run(
                ["git", "-C", local_dir, "rev-list", f"HEAD..origin/{branch}", "--count"],
                capture_output=True, text=True, check=True
            )
            count = int(result.stdout.strip())
            return count > 0
        except Exception as e:
            logger.error(f"Failed to check for changes: {e}")
            return False
    