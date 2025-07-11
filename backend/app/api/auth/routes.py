from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService

bp = Blueprint('auth', __name__)
auth_service = AuthService()

@bp.route('/register', methods=['POST'])
def register():
    """用户注册"""
    data = request.json
    
    if not data:
        return jsonify({'error': '无效的请求数据'}), 400
        
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not username or not email or not password:
        return jsonify({'error': '缺少必要的字段'}), 400
        
    success, result = auth_service.register_user(username, email, password)
    
    if success:
        return jsonify({'message': '注册成功', 'user': result.to_dict()}), 201
    else:
        return jsonify({'error': result}), 400

@bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.json
    
    if not data:
        return jsonify({'error': '无效的请求数据'}), 400
        
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': '缺少必要的字段'}), 400
        
    success, result = auth_service.authenticate_user(username, password)
    
    if success:
        return jsonify({'message': '登录成功', **result}), 200
    else:
        return jsonify({'error': result}), 401

@bp.route('/activate_card', methods=['POST'])
def activate_card():
    """激活卡密"""
    # 验证token
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': '未提供认证信息'}), 401
        
    token = token.replace('Bearer ', '')
    user = auth_service.verify_token(token)
    if not user:
        return jsonify({'error': '无效的认证信息'}), 401
        
    data = request.json
    
    if not data:
        return jsonify({'error': '无效的请求数据'}), 400
        
    card_code = data.get('card_code')
    
    if not card_code:
        return jsonify({'error': '缺少卡密'}), 400
        
    success, message = auth_service.activate_card(user.id, card_code)
    
    if success:
        return jsonify({'message': message}), 200
    else:
        return jsonify({'error': message}), 400    