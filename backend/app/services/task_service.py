from app.models import Task, Comment
from app import db
from .comment_service import CommentService
import requests
import json
import time
from datetime import datetime

class TaskService:
    def __init__(self):
        self.comment_service = CommentService()
    
    def create_task(self, user_id, name, room_url):
        """创建新任务"""
        task = Task(
            user_id=user_id,
            name=name,
            room_url=room_url,
            status='pending'
        )
        
        db.session.add(task)
        db.session.commit()
        
        return task
    
    def get_task(self, task_id):
        """获取任务"""
        task = Task.query.get(task_id)
        return task
    
    def get_tasks_by_user(self, user_id):
        """获取用户的所有任务"""
        tasks = Task.query.filter_by(user_id=user_id).all()
        return [task.to_dict() for task in tasks]
    
    def update_task_status(self, task_id, status):
        """更新任务状态"""
        task = Task.query.get(task_id)
        if not task:
            return False
            
        task.status = status
        task.updated_at = datetime.utcnow()
        db.session.commit()
        
        return True
    
    def start_task(self, task_id):
        """启动任务"""
        task = Task.query.get(task_id)
        if not task:
            return False, "任务不存在"
            
        if task.status == 'running':
            return False, "任务已在运行中"
            
        # 更新任务状态
        task.status = 'running'
        task.updated_at = datetime.utcnow()
        db.session.commit()
        
        # 启动评论抓取（在实际应用中，这可能是一个Celery任务）
        # 这里简化处理，直接调用模拟的抓取函数
        # 在实际应用中，这应该是一个后台任务
        # fetch_comments.delay(task_id)
        
        return True, "任务已启动"
    
    def stop_task(self, task_id):
        """停止任务"""
        task = Task.query.get(task_id)
        if not task:
            return False, "任务不存在"
            
        if task.status != 'running':
            return False, "任务未在运行中"
            
        # 更新任务状态
        task.status = 'stopped'
        task.updated_at = datetime.utcnow()
        db.session.commit()
        
        return True, "任务已停止"
    
    def delete_task(self, task_id):
        """删除任务"""
        task = Task.query.get(task_id)
        if not task:
            return False, "任务不存在"
            
        # 删除关联的评论
        Comment.query.filter_by(task_id=task_id).delete()
        
        # 删除任务
        db.session.delete(task)
        db.session.commit()
        
        return True, "任务已删除"    