from app.models import Comment, Task
from app import db
from .analysis_service import AnalysisService
from .voice_service import VoiceService
import time

class CommentService:
    def __init__(self):
        self.analysis_service = AnalysisService()
        self.voice_service = VoiceService()
    
    def save_comments(self, task_id, comments_data):
        """保存评论数据"""
        task = Task.query.get(task_id)
        if not task:
            return False, "任务不存在"
            
        saved_comments = []
        for comment_data in comments_data:
            # 检查评论是否已存在
            existing_comment = Comment.query.filter_by(
                task_id=task_id,
                user_id=comment_data.get('user_id'),
                content=comment_data.get('content')
            ).first()
            
            if existing_comment:
                continue
                
            # 创建新评论
            comment = Comment(
                content=comment_data.get('content'),
                user_name=comment_data.get('user_name'),
                user_id=comment_data.get('user_id'),
                user_avatar=comment_data.get('user_avatar'),
                task_id=task_id
            )
            
            db.session.add(comment)
            saved_comments.append(comment)
        
        # 提交事务
        db.session.commit()
        
        # 异步分析评论
        if saved_comments:
            self.analysis_service.analyze_comments(saved_comments, task_id)
            
        return True, saved_comments
    
    def get_comments_by_task(self, task_id, limit=100, offset=0):
        """获取任务的评论"""
        task = Task.query.get(task_id)
        if not task:
            return False, "任务不存在"
            
        comments = Comment.query.filter_by(task_id=task_id) \
            .order_by(Comment.created_at.desc()) \
            .limit(limit) \
            .offset(offset) \
            .all()
            
        return True, [comment.to_dict() for comment in comments]
    
    def generate_voice_for_comment(self, comment_id, user_id):
        """为评论生成语音"""
        comment = Comment.query.get(comment_id)
        if not comment:
            return False, "评论不存在"
            
        voice_url = self.voice_service.generate_voice(
            comment.content, 
            comment.task_id, 
            user_id
        )
        
        if voice_url:
            return True, voice_url
        else:
            return False, "语音生成失败"    