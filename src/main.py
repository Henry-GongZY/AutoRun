import logging
from src.config import settings
from src.clients.feishu_client import FeishuClient
from src.core.task import BatchConfig
from src.core.runner import TaskRunner

# 配置日志
logging.basicConfig(level=settings.log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    logger.info("AutoRun service starting...")

    # 1. 加载任务配置
    try:
        config = BatchConfig.from_file("tasks.json")
        logger.info(f"Loaded {len(config.tasks)} tasks from tasks.json")
    except Exception as e:
        logger.error(f"Failed to load tasks.json: {e}")
        return

    # 2. 初始化飞书客户端
    feishu = FeishuClient(settings.feishu_app_id, settings.feishu_app_secret)

    # 3. 定义当在飞书消息中检测到路径时的处理逻辑
    def on_feishu_path_received(path, data):
        # 获取发送消息的 chat_id 以便回复
        chat_id = data.event.message.chat_id
        
        # 寻找匹配的任务
        matching_task = next((t for t in config.tasks if t.local_dir == path), None)
        
        if matching_task:
            feishu.send_text_message("chat_id", chat_id, f"🔍 检测到匹配任务: {matching_task.name}，正在启动...")
            
            # 执行任务
            runner = TaskRunner(tasks=[matching_task])
            try:
                runner.run_all()
                feishu.send_text_message("chat_id", chat_id, f"✅ 任务执行成功: {matching_task.name}")
            except Exception as e:
                feishu.send_text_message("chat_id", chat_id, f"❌ 任务执行失败: {str(e)}")
        else:
            logger.warning(f"No task found for path: {path}")
            feishu.send_text_message("chat_id", chat_id, f"⚠️ 未找到与目录 '{path}' 关联的任务，请检查 tasks.json 配置。")

    # 4. 启动长连接监听器（这将阻塞当前线程）
    try:
        feishu.start_event_listener(on_feishu_path_received)
    except KeyboardInterrupt:
        logger.info("Service stopped by user.")
    except Exception as e:
        logger.error(f"Listener error: {e}")

if __name__ == "__main__":
    main()
