from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/upland-webhook', methods=['POST'])
def upland_webhook():
    data = request.json
    logger.info(f"Recebido do Upland: {data}")

    code = data['data']['code']
    user_id = data['data']['userId']
    access_token = data['data']['accessToken']

    logger.info(f"Código: {code}, UserID: {user_id}, AccessToken: {access_token}")

    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
