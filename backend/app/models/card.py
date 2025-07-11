from datetime import datetime, timedelta
from app import db

class Card(db.Model):
    __tablename__ = 'cards'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(64), unique=True, index=True)
    is_used = db.Column(db.Boolean, default=False)
    expires_at = db.Column(db.DateTime)
    uses_limit = db.Column(db.Integer, default=0)
    uses_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关联用户
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def is_valid(self):
        """检查卡密是否有效"""
        return (not self.is_used and 
                self.expires_at > datetime.utcnow() and 
                (self.uses_limit == 0 or self.uses_count < self.uses_limit))
    
    def use(self):
        """使用卡密"""
        if not self.is_valid():
            return False
            
        self.uses_count += 1
        if self.uses_limit > 0 and self.uses_count >= self.uses_limit:
            self.is_used = True
            
        db.session.commit()
        return True
    
    @staticmethod
    def generate_card(days=30, uses_limit=0):
        """生成新卡密"""
        import uuid
        code = str(uuid.uuid4()).replace('-', '')[:16]
        card = Card(
            code=code,
            expires_at=datetime.utcnow() + timedelta(days=days),
            uses_limit=uses_limit
        )
        db.session.add(card)
        db.session.commit()
        return card
    
    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'is_used': self.is_used,
            'expires_at': self.expires_at.strftime('%Y-%m-%d %H:%M:%S'),
            'uses_limit': self.uses_limit,
            'uses_count': self.uses_count,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'user_id': self.user_id,
            'is_valid': self.is_valid()
        }    