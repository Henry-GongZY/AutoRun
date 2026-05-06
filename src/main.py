import logging
import time
import threading
from src.config import settings
from src.clients.feishu_client import FeishuClient
from src.core.task import BatchConfig
from src.core.runner import TaskRunner
from src.utils.git_helper import GitHelper

# 配置日志
logging.basicConfig(level=settings.log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_sleep_interval():
    """根据当前时间计算轮询间隔（秒）"""
    current_hour = time.localtime().tm_hour
    
    if 9 <= current_hour < 20:
        # 9点 - 20点：5分钟一次
        return 300
    elif (7 <= current_hour < 9) or (20 <= current_hour < 23):
        # 7点 - 9点，20点 - 23点：15分钟一次
        return 900
    else:
        # 其余时间：不同步（这里设置为每小时检查一次，直到进入活跃时段）
        return 3600

def git_monitor_loop(config: BatchConfig):
    """后台轮询线程：动态频率监控 Git 更新"""
    logger.info("Dynamic Git monitor started.")
    while True:
        interval = get_sleep_interval()
        
        # 只有在非休眠时段（间隔小于3600秒）才执行同步逻辑
        if interval < 3600:
            for task in config.tasks:
                if not task.git_url:
                    continue
                
                local_v = GitHelper.local_version(task.local_dir)
                remote_v = GitHelper.remote_version(task.local_dir, task.branch)

                if remote_v and local_v != remote_v:
                    logger.info(f"Update detected for {task.name}. Starting background sync...")
                    TaskRunner.syncing_paths.add(task.local_dir)
                    try:
                        GitHelper.ensure_repo(task.local_dir, task.git_url, task.branch)
                        logger.info(f"Background sync finished for {task.name}")
                    finally:
                        TaskRunner.syncing_paths.discard(task.local_dir)
        else:
            logger.debug("System in idle period, skipping sync.")

        time.sleep(interval)

def main():
    logger.info("AutoRun service starting...")

    # 1. 加载任务配置
    try:
        config = BatchConfig.from_file("tasks.json")
    except Exception as e:
        logger.error(f"Failed to load tasks.json: {e}")
        return

    # 2. 启动后台 Git 监控线程
    monitor_thread = threading.Thread(target=git_monitor_loop, args=(config,), daemon=True)
    monitor_thread.start()

    # 3. 初始化飞书客户端
    feishu = FeishuClient(settings.feishu_app_id, settings.feishu_app_secret)

    # 4. 定义飞书消息处理逻辑
    def on_feishu_path_received(path, data):
        chat_id = data.event.message.chat_id
        matching_task = next((t for t in config.tasks if t.local_dir == path), None)
        
        if not matching_task:
            feishu.send_text_message("chat_id", chat_id, f"⚠️ 未找到与目录 '{path}' 关联的任务。")
            return

        # 执行前检查是否正在同步
        runner = TaskRunner(tasks=[matching_task])
        if runner.is_syncing(matching_task.local_dir):
            feishu.send_text_message("chat_id", chat_id, f"⏳ 项目 '{matching_task.name}' 正在进行后台 Git 同步，请稍后再试。")
            return

        # 开始执行
        feishu.send_text_message("chat_id", chat_id, f"🚀 正在执行任务: {matching_task.name}...")
        try:
            runner.run_task(matching_task)
            feishu.send_text_message("chat_id", chat_id, f"✅ 任务执行成功: {matching_task.name}")
        except Exception as e:
            feishu.send_text_message("chat_id", chat_id, f"❌ 执行出错: {str(e)}")

    # 5. 启动飞书事件监听
    try:
        feishu.start_event_listener(on_feishu_path_received)
    except KeyboardInterrupt:
        logger.info("Service stopped.")

if __name__ == "__main__":
    main()
