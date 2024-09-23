from flask import Flask, jsonify
from flask_cors import CORS
from .routes import main as routes

def create_app():
    """
    Cria e configura a aplicação Flask.

    Retorna:
        Flask: Instância da aplicação Flask configurada.
    """
    app = Flask(__name__, static_url_path='/static')
    CORS(app, resources={r"/*": {"origins": "*"}})  # Habilita CORS para todas as origens
    app.register_blueprint(routes)  # Registra as rotas definidas no blueprint

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)  # Executa a aplicação em modo debug
