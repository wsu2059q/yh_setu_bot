import requests
import json
import logging
import time
from config import setu_api_url
logging.basicConfig(level=logging.DEBUG)
class SetuAPIClient:
    def get_setu(self, tag=None, keyword=None, r18=0, num=1, max_retries=1):
        params = {
            "r18": r18,
            "num": num
        }
        if tag:
            params["tag"] = tag
        if keyword:
            params["keyword"] = keyword
        for attempt in range(max_retries + 1):
            try:
                response = requests.get(setu_api_url, params=params, timeout=3)
                logging.debug(f"API状态码: {response.status_code}")
                if response.status_code == 200:
                    return response.json()
                else:
                    logging.error(f"API响应失败 (Attempt {attempt + 1}): {response.text}")
                    if attempt < max_retries:
                        logging.info(f"重试中...")
                        time.sleep(0.5)
                    else:
                        return {"error": "API请求失败"}
            except requests.exceptions.RequestException as e:
                logging.error(f"API响应失败 (Attempt {attempt + 1}): {e}")
                if attempt < max_retries:
                    logging.info(f"重试中...")
                    time.sleep(0.5)
                else:
                    return {"error": "请求异常"}

class YunhuAPIClient:
    pass
