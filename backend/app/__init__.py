<from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from celery import Celery
from config import config

db = SQLAlchemy()
socketio = SocketIO()
celery = Celery(__name__, broker=config['development'].CELERY_BROKER_URL)

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    db.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")
    celery.conf.update(app.config)
    
    # 注册蓝图
    from .api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # 错误处理
    from .utils import handle_errors
    handle_errors(app)
    
    # 确保模型被创建
    with app.app_context():
        db.create_all()
    
    return app