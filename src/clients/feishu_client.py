import lark_oapi as lark
from lark_oapi.api.im.v1 import CreateMessageRequest, CreateMessageRequestBody
import logging

class FeishuClient:
    def __init__(self, app_id: str, app_secret: str):
        self.client = lark.Client.builder() \
            .app_id(app_id) \
            .app_secret(app_secret) \
            .log_level(lark.LogLevel.INFO) \
            .build()

    def send_text_message(self, receive_id_type: str, receive_id: str, content: str):
        """
        发送文本消息
        :param receive_id_type: open_id, user_id, union_id, email, chat_id
        :param receive_id: 接收者 ID
        :param content: 消息内容
        """
        request = CreateMessageRequest.builder() \
            .receive_id_type(receive_id_type) \
            .request_body(CreateMessageRequestBody.builder() \
                .receive_id(receive_id) \
                .msg_type("text") \
                .content(f'{{"text":"{content}"}}') \
                .build()) \
            .build()

        response = self.client.im.v1.message.create(request)

        if not response.success():
            logging.error(f"Feishu send message failed: {response.code}, {response.msg}, {response.error}")
            return False
        
        return True
