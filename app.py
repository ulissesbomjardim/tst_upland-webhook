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

    # Verifica se a chave 'data' está no payload
    if 'data' in data:
        code = data['data'].get('code', 'N/A')
        user_id = data['data'].get('userId', 'N/A')
        access_token = data['data'].get('accessToken', 'N/A')
        
        logger.info(f"Código: {code}, UserID: {user_id}, AccessToken: {access_token}")
    else:
        logger.warning("Chave 'data' ausente no payload recebido")

    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
