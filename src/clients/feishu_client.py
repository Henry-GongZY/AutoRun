import lark_oapi as lark
from lark_oapi.api.im.v1 import CreateMessageRequest, CreateMessageRequestBody, P2ImMessageReceiveV1
import logging
import json
import re

logger = logging.getLogger(__name__)

class FeishuClient:
    def __init__(self, app_id: str, app_secret: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self.client = lark.Client.builder() \
            .app_id(app_id) \
            .app_secret(app_secret) \
            .log_level(lark.LogLevel.INFO) \
            .build()

    def send_text_message(self, receive_id_type: str, receive_id: str, content: str):
        """发送文本消息"""
        request = CreateMessageRequest.builder() \
            .receive_id_type(receive_id_type) \
            .request_body(CreateMessageRequestBody.builder() \
                .receive_id(receive_id) \
                .msg_type("text") \
                .content(json.dumps({"text": content})) \
                .build()) \
            .build()

        response = self.client.im.v1.message.create(request)
        if not response.success():
            logger.error(f"Feishu send message failed: {response.code}, {response.msg}")
            return False
        return True

    def start_event_listener(self, on_path_received):
        """
        启动事件长连接监听
        :param on_path_received: 接收到路径时的回调函数，格式为 callback(path, message_data)
        """
        event_handler = lark.EventDispatcherHandler.builder("", "") \
            .register_p2_im_message_receive_v1(lambda data: self._handle_message(data, on_path_received)) \
            .build()

        # 启动长连接客户端
        ws_client = lark.WsClient(self.app_id, self.app_secret, event_handler=event_handler, log_level=lark.LogLevel.INFO)
        logger.info("Feishu WebSocket listener starting...")
        ws_client.start()

    def _handle_message(self, data: P2ImMessageReceiveV1, callback):
        """处理接收到的消息事件"""
        msg = data.event.message
        # 飞书消息内容是 JSON 字符串，例如 {"text":"@机器人 /some/path"}
        content_raw = json.loads(msg.content)
        text = content_raw.get("text", "")

        logger.info(f"Received message: {text}")

        # 简单的正则匹配：识别以 / 或 ./ 或 ../ 开头的路径信息
        # 您可以根据实际需求调整此正则
        path_pattern = r'((?:\.{0,2}/)[\w\.\-/]+)'
        match = re.search(path_pattern, text)

        if match:
            path = match.group(1)
            logger.info(f"Path detected in message: {path}")
            # 回传路径和消息元数据（用于后续回复）
            callback(path, data)
        
        return None
