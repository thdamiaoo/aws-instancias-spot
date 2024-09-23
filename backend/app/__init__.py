from flask import Flask

def create_app():
    """
    Retorna:
        app: A instância da aplicação Flask configurada.
    """
    app = Flask(__name__, static_url_path='/static')

    # Importa e registra as rotas do aplicativo
    from .routes import main as routes
    app.register_blueprint(routes)

    return app
