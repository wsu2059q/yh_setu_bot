import json
import requests
import logging
from config import yunhu_token
from utils.api_client import SetuAPIClient  

class YunhuHandler:
    def __init__(self, data: dict):
        logging.debug(f"元数据: {data}")
        self.data = data
        self.commandName = data.get("event", {}).get("message", {}).get("commandName", "")
        self.message_content = data.get("event", {}).get("message", {}).get("content", {}).get("text", "")
        self.sender_id = data.get("event", {}).get("sender", {}).get("senderId", "")
        self.sender_type = data.get("event", {}).get("sender", {}).get("senderType", "")
        self.recv_id = data.get("event", {}).get("message", {}).get("chatId", "")
        self.recv_type = data.get("event", {}).get("message", {}).get("chatType", "")
        self.setu_client = SetuAPIClient()
        self.form = data.get('event', {}).get('message', {}).get('content', {}).get('formJson', {})
        self.content_type = data.get("event", {}).get("message", {}).get("content", {}).get("type", "")
        self.content = data.get("event", {}).get("message", {}).get("content", {}).get("formJson", "")

    def send_message(self, content_type, content):
        if self.recv_type == "group":
            recv_type = "group"
            recv_id = self.recv_id
        else:
            recv_type = "user"
            recv_id = self.sender_id
        headers = {'Content-Type': 'application/json'}
        payload = {
            "recvId": recv_id,
            "recvType": recv_type,
            "contentType": content_type,
            "content": {}
        }

        if content_type == 'text':
            payload['content']['text'] = content
        elif content_type == 'html':
            payload['content']['text'] = content

        response = requests.post(f"https://chat-go.jwzhd.com/open-apis/v1/bot/send?token={yunhu_token}", headers=headers, data=json.dumps(payload))
        return response.json()

    def handle_command(self):
        logging.debug(f"指令: {self.commandName}")
        if self.commandName == "色图":
            tag = None
            keyword = None
            search_type = self.content.get('czwmnr', {}).get('selectValue', None)
            if search_type == "标签":
                tag = self.content.get('dshcpo', {}).get('value', None)
            elif search_type == "作者":
                keyword = self.content.get('dshcpo', {}).get('value', None)
            logging.debug(f"标签: {tag}")
            logging.debug(f"作者: {keyword}")
            try:
                response = self.setu_client.get_setu(tag=tag, keyword=keyword)
                logging.debug(f"API回复: {response}")
                if "data" in response and response["data"]:
                    setu_data = response["data"][0]
                    title = setu_data.get("title", "无标题")
                    author = setu_data.get("author", "未知作者")
                    width = setu_data.get("width", "未知宽度")
                    height = setu_data.get("height", "未知高度")
                    tags = ", ".join(setu_data.get("tags", []))
                    urls = setu_data.get("urls", {})
                    original_url = urls.get("original", "")

                    content = (
                        f'<img src="{original_url}" alt="图片"><br><hr>'
                        f'<strong>标题:</strong> {title}<br>'
                        f'<strong>作者:</strong> {author}<br>'
                        f'<strong>尺寸:</strong> {width}x{height}<br>'
                        f'<strong>标签:</strong> {tags}'
                    )
                    self.send_message("html", content)
                else:
                    self.send_message("text", "找不到相关的色图")
            except Exception as e:
                logging.error(f"错误: {e}")
                self.send_message("text", "请求失败，请稍后再试")
        else:
            self.send_message("text", "未知指令")