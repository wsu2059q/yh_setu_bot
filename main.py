from flask import Flask, request, jsonify
from handler import YunhuHandler
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if data:
        handler = YunhuHandler(data)
        handler.handle_command()
        return jsonify({"status": "success"}), 200
    logging.error("未收到数据")
    return jsonify({"status": "error"}), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6888)