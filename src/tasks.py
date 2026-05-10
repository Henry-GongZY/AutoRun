from .core.task import BatchTask

# 定义公共变量
REPOS_DIR = "./repos"
INPUT_PATH = "/Users/shinano/Downloads/test/batch_input.jsonl"
OUTPUT_PATH = "/Users/shinano/Downloads/test/batch_output.jsonl"

# 任务列表
TASKS = [
    BatchTask(
        name="",
        git_url="",
        local_dir=f"{REPOS_DIR}",
        commands=[
            
        ],
        branch="main"
    ),
    BatchTask(
        name="Update Documentation",
        git_url="https://github.com/larksuite/oapi-sdk-python.git",
        local_dir=f"{REPOS_DIR}/feishu_sdk",
        commands=[
            f"python simu.py -i {INPUT_PATH} -o {OUTPUT_PATH}"
        ],
        branch="v2"
    )
]
