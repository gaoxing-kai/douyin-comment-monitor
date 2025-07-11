from flask import Blueprint, request, jsonify
from app.services.task_service import TaskService
from app.services.auth_service import AuthService

bp = Blueprint('tasks', __name__)
task_service = TaskService()
auth_service = AuthService()

@bp.route('/tasks', methods=['GET'])
def get_tasks():
    """获取用户的所有任务"""
    # 验证token
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': '未提供认证信息'}), 401
        
    token = token.replace('Bearer ', '')
    user = auth_service.verify_token(token)
    if not user:
        return jsonify({'error': '无效的认证信息'}), 401
        
    tasks = task_service.get_tasks_by_user(user.id)
    return jsonify({'tasks': tasks}), 200

@bp.route('/tasks', methods=['POST'])
def create_task():
    """创建新任务"""
    # 验证token
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': '未提供认证信息'}), 401
        
    token = token.replace('Bearer ', '')
    user = auth_service.verify_token(token)
    if not user:
        return jsonify({'error': '无效的认证信息'}), 401
        
    # 获取任务数据
    data = request.json
    if not data:
        return jsonify({'error': '无效的请求数据'}), 400
        
    name = data.get('name')
    room_url = data.get('room_url')
    
    if not name or not room_url:
        return jsonify({'error': '缺少必要的字段'}), 400
        
    task = task_service.create_task(user.id, name, room_url)
    return jsonify({'task': task.to_dict()}), 201

@bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """获取单个任务"""
    # 验证token
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': '未提供认证信息'}), 401
        
    token = token.replace('Bearer ', '')
    user = auth_service.verify_token(token)
    if not user:
        return jsonify({'error': '无效的认证信息'}), 401
        
    task = task_service.get_task(task_id)
    if not task:
        return jsonify({'error': '任务不存在'}), 404
        
    if task.user_id != user.id:
        return jsonify({'error': '无权访问此任务'}), 403
        
    return jsonify({'task': task.to_dict()}), 200

@bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """更新任务"""
    # 验证token
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': '未提供认证信息'}), 401
        
    token = token.replace('Bearer ', '')
    user = auth_service.verify_token(token)
    if not user:
        return jsonify({'error': '无效的认证信息'}), 401
        
    task = task_service.get_task(task_id)
    if not task:
        return jsonify({'error': '任务不存在'}), 404
        
    if task.user_id != user.id:
        return jsonify({'error': '无权访问此任务'}), 403
        
    # 获取更新数据
    data = request.json
    if not data:
        return jsonify({'error': '无效的请求数据'}), 400
        
    if 'name' in data:
        task.name = data['name']
        
    if 'room_url' in data:
        task.room_url = data['room_url']
        
    if 'status' in data:
        task.status = data['status']
        
    task.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({'task': task.to_dict()}), 200

@bp.route('/tasks/<int:task_id>/start', methods=['POST'])
def start_task(task_id):
    """启动任务"""
    # 验证token
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': '未提供认证信息'}), 401
        
    token = token.replace('Bearer ', '')
    user = auth_service.verify_token(token)
    if not user:
        return jsonify({'error': '无效的认证信息'}), 401
        
    success, message = task_service.start_task(task_id)
    
    if success:
        return jsonify({'message': message}), 200
    else:
        return jsonify({'error': message}), 400

@bp.route('/tasks/<int:task_id>/stop', methods=['POST'])
def stop_task(task_id):
    """停止任务"""
    # 验证token
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': '未提供认证信息'}), 401
        
    token = token.replace('Bearer ', '')
    user = auth_service.verify_token(token)
    if not user:
        return jsonify({'error': '无效的认证信息'}), 401
        
    success, message = task_service.stop_task(task_id)
    
    if success:
        return jsonify({'message': message}), 200
    else:
        return jsonify({'error': message}), 400

@bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """删除任务"""
    # 验证token
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': '未提供认证信息'}), 401
        
    token = token.replace('Bearer ', '')
    user = auth_service.verify_token(token)
    if not user:
        return jsonify({'error': '无效的认证信息'}), 401
        
    success, message = task_service.delete_task(task_id)
    
    if success:
        return jsonify({'message': message}), 200
    else:
        return jsonify({'error': message}), 400    