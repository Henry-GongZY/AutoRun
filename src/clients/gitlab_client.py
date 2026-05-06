import gitlab
import logging

class GitLabClient:
    def __init__(self, url: str, private_token: str):
        self.gl = gitlab.Gitlab(url=url, private_token=private_token)
        try:
            self.gl.auth()
        except Exception as e:
            logging.error(f"Failed to authenticate with GitLab: {e}")

    def get_project(self, project_id: int):
        """获取项目对象"""
        try:
            return self.gl.projects.get(project_id)
        except Exception as e:
            logging.error(f"Failed to get project {project_id}: {e}")
            return None

    def list_projects(self):
        """列出所有项目"""
        return self.gl.projects.list(all=True)
