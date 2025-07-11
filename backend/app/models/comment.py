from datetime import datetime
from app import db

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    user_name = db.Column(db.String(128))
    user_id = db.Column(db.String(64))
    user_avatar = db.Column(db.String(256))
    sentiment = db.Column(db.String(16), default='neutral')  # positive, negative, neutral
    keywords = db.Column(db.JSON, default=[])
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关联任务
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))
    
    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'user_name': self.user_name,
            'user_id': self.user_id,
            'user_avatar': self.user_avatar,
            'sentiment': self.sentiment,
            'keywords': self.keywords,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'task_id': self.task_id
        }    