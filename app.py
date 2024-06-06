from flask import Flask, request, jsonify
import logging
import os
from firebase_admin import credentials, db, initialize_app
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env (opcional)
load_dotenv()

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configurar credenciais do Firebase a partir das variáveis de ambiente
firebase_config = {
    "type": "service_account",
    "project_id": os.getenv("FIREBASE_PROJECT_ID"),
    "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
    "private_key": os.getenv("FIREBASE_PRIVATE_KEY").replace('\\n', '\n'),
    "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
    "client_id": os.getenv("FIREBASE_CLIENT_ID"),
    "auth_uri": os.getenv("FIREBASE_AUTH_URI"),
    "token_uri": os.getenv("FIREBASE_TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("FIREBASE_AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_X509_CERT_URL")
}

# Inicializa o app do Firebase com as credenciais
cred = credentials.Certificate(firebase_config)
initialize_app(cred, {
    'databaseURL': 'https://dont-kill-the-rabbit-9747314.firebaseio.com/'
})

# Função para encontrar o usuário pelo upltoken
def find_user_by_upltoken(upltoken):
    ref = db.reference('users')
    users = ref.get()

    for user_id, user_info in users.items():
        if 'upltoken' in user_info and user_info['upltoken'] == upltoken:
            return user_id, user_info
    
    return None, None

# Função para atualizar a autenticação do usuário
def update_user_authentication(upltoken, new_authentication_info):
    user_id, user_info = find_user_by_upltoken(upltoken)

    if user_id:
        user_ref = db.reference(f'users/{user_id}/Upland/AuthenticationSuccess')
        user_ref.update(new_authentication_info)
        logger.info(f"Usuário {user_id} atualizado com sucesso.")
    else:
        logger.warning(f"Usuário com upltoken {upltoken} não encontrado.")

app = Flask(__name__)

@app.route('/upland-webhook', methods=['POST'])
def upland_webhook():
    data = request.json
    logger.info(f"Recebido do Upland: {data}")

    # Verifica se a chave 'data' está no payload
    if 'data' in data:
        upltoken = data['data'].get('code', 'N/A')
        user_id = data['data'].get('userId', 'N/A')
        access_token = data['data'].get('accessToken', 'N/A')
        app_id = data['data'].get('appId', 'N/A')
        code = data['data'].get('code', 'N/A')

        logger.info(f"Código: {upltoken}, UserID: {user_id}, AccessToken: {access_token}, AppID: {app_id}")

        # Informações de autenticação a serem atualizadas
        new_authentication_info = {
            'accessToken': access_token,
            'appId': app_id,
            'userId': user_id,
            'code': code
        }

        # Atualiza o usuário no Firebase
        update_user_authentication(upltoken, new_authentication_info)
        
    else:
        logger.warning("Chave 'data' ausente no payload recebido")

    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
