from flask import Blueprint
from .auth.routes import bp as auth_bp
from .tasks.routes import bp as tasks_bp
from .comments.routes import bp as comments_bp
from .voice.routes import bp as voice_bp

api_bp = Blueprint('api', __name__)

# 注册子蓝图
api_bp.register_blueprint(auth_bp)
api_bp.register_blueprint(tasks_bp)
api_bp.register_blueprint(comments_bp)
api_bp.register_blueprint(voice_bp)    