from datetime import datetime
from app import db

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    room_url = db.Column(db.String(256))
    status = db.Column(db.String(32), default='pending')  # pending, running, stopped, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联用户
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # 关联评论
    comments = db.relationship('Comment', backref='task', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'room_url': self.room_url,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'user_id': self.user_id,
            'comments_count': self.comments.count()
        }    