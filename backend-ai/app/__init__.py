from flask import Flask
from .routes.user import bp
from flask_cors import CORS
def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    CORS(app)
    # Đăng ký blueprint
    app.register_blueprint(bp, url_prefix='/api/users')

    return app
