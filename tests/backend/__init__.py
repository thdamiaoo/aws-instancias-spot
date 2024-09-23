from flask import Flask

def create_app():
    app = Flask(__name__, static_url_path='/static')

    from .routes import main as routes
    app.register_blueprint(routes)

    return app
