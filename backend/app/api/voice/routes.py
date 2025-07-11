from flask import Blueprint, request, jsonify, send_from_directory
from app.services.voice_service import VoiceService
from app.services.auth_service import AuthService
from app.config import config
import os

bp = Blueprint('voice', __name__)
voice_service = VoiceService()
auth_service = AuthService()

@bp.route('/voices/<int:task_id>/<path:filename>', methods=['GET'])
def get_voice_file(task_id, filename):
    """获取语音文件"""
    # 验证token
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': '未提供认证信息'}), 401
        
    token = token.replace('Bearer ', '')
    user = auth_service.verify_token(token)
    if not user:
        return jsonify({'error': '无效的认证信息'}), 401
        
    # 检查文件是否存在
    voice_dir = os.path.join(config['VOICE_FILES_DIR'], str(task_id))
    
    if not os.path.exists(voice_dir):
        return jsonify({'error': '文件不存在'}), 404
        
    if not os.path.isfile(os.path.join(voice_dir, filename)):
        return jsonify({'error': '文件不存在'}), 404
        
    return send_from_directory(voice_dir, filename)    