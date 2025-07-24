from flask import Flask
from .routes.user import bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')

    # Đăng ký blueprint
    app.register_blueprint(bp, url_prefix='/api/users')

    return app
