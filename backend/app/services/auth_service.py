from app.models import User, Card
from app import db
import jwt
from datetime import datetime, timedelta
from flask import current_app

class AuthService:
    def __init__(self):
        pass
    
    def register_user(self, username, email, password):
        """注册新用户"""
        # 检查用户名是否已存在
        if User.query.filter_by(username=username).first():
            return False, "用户名已存在"
            
        # 检查邮箱是否已存在
        if User.query.filter_by(email=email).first():
            return False, "邮箱已存在"
            
        # 创建新用户
        user = User(
            username=username,
            email=email,
            password=password
        )
        
        db.session.add(user)
        db.session.commit()
        
        return True, user
    
    def authenticate_user(self, username, password):
        """验证用户并生成token"""
        user = User.query.filter_by(username=username).first()
        
        if user and user.verify_password(password):
            # 生成token
            token = self.generate_token(user.id)
            return True, {'user': user.to_dict(), 'token': token}
        else:
            return False, "用户名或密码错误"
    
    def generate_token(self, user_id, expires_in=3600):
        """生成JWT token"""
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(seconds=expires_in)
        }
        
        token = jwt.encode(
            payload,
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )
        
        return token
    
    def verify_token(self, token):
        """验证JWT token"""
        try:
            payload = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256']
            )
            
            user_id = payload.get('user_id')
            if not user_id:
                return None
                
            user = User.query.get(user_id)
            return user
            
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def activate_card(self, user_id, card_code):
        """激活卡密"""
        user = User.query.get(user_id)
        if not user:
            return False, "用户不存在"
            
        card = Card.query.filter_by(code=card_code).first()
        if not card:
            return False, "卡密不存在"
            
        if card.is_used:
            return False, "卡密已被使用"
            
        if card.user_id and card.user_id != user_id:
            return False, "卡密已被其他用户绑定"
            
        if not card.is_valid():
            return False, "卡密已过期或已达到使用次数限制"
            
        # 绑定卡密到用户
        card.user_id = user_id
        card.is_used = True
        db.session.commit()
        
        return True, "卡密激活成功"    