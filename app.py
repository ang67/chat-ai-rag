from flask import Flask
from flask_cors import CORS
from routes.chat import chat_bp
from config import FLASK_PORT

# 1. Créer l'app Flask
app = Flask(__name__)

# 2. Configurer CORS
CORS(app=app)
# CORS(app=app, origins=['http://localhost:5173'])

# 3. Enregistrer le blueprint
app.register_blueprint(chat_bp, url_prefix='/chat')

# 4. Route de test (optionnelle)
@app.route('/')
def home():
    return {'message': 'Backend RAG API'}

# 5. Lancer le serveur
if __name__ == '__main__':
    app.run(host='localhost', port=FLASK_PORT, debug=True)