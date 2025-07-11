from flask import Blueprint, request, jsonify
from app.services.comment_service import CommentService
from app.services.auth_service import AuthService
from app.extensions import socketio

bp = Blueprint('comments', __name__)
comment_service = CommentService()
auth_service = AuthService()

@bp.route('/tasks/<int:task_id>/comments', methods=['GET'])
def get_comments(task_id):
    """获取任务的评论"""
    # 验证token
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': '未提供认证信息'}), 401
        
    token = token.replace('Bearer ', '')
    user = auth_service.verify_token(token)
    if not user:
        return jsonify({'error': '无效的认证信息'}), 401
        
    # 获取参数
    limit = request.args.get('limit', 100, type=int)
    offset = request.args.get('offset', 0, type=int)
    
    success, comments = comment_service.get_comments_by_task(task_id, limit, offset)
    
    if success:
        return jsonify({'comments': comments}), 200
    else:
        return jsonify({'error': comments}), 404

@bp.route('/tasks/<int:task_id>/comments', methods=['POST'])
def save_comments(task_id):
    """保存评论"""
    # 验证token
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': '未提供认证信息'}), 401
        
    token = token.replace('Bearer ', '')
    user = auth_service.verify_token(token)
    if not user:
        return jsonify({'error': '无效的认证信息'}), 401
        
    # 获取评论数据
    data = request.json
    if not data or 'comments' not in data:
        return jsonify({'error': '无效的请求数据'}), 400
        
    success, comments = comment_service.save_comments(task_id, data['comments'])
    
    if success:
        return jsonify({'message': '评论保存成功', 'comments': [c.to_dict() for c in comments]}), 201
    else:
        return jsonify({'error': comments}), 400

@bp.route('/comments/<int:comment_id>/voice', methods=['POST'])
def generate_voice(comment_id):
    """为评论生成语音"""
    # 验证token
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': '未提供认证信息'}), 401
        
    token = token.replace('Bearer ', '')
    user = auth_service.verify_token(token)
    if not user:
        return jsonify({'error': '无效的认证信息'}), 401
        
    success, voice_url = comment_service.generate_voice_for_comment(comment_id, user.id)
    
    if success:
        return jsonify({'voice_url': voice_url}), 200
    else:
        return jsonify({'error': voice_url}), 400    