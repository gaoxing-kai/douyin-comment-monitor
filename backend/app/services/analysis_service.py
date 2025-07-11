import requests
import json
from app.extensions import socketio
from app.config import config

class AnalysisService:
    def __init__(self):
        self.api_key = config['DEEPSEEK_API_KEY']
        self.api_url = config['DEEPSEEK_API_URL']
    
    def analyze_comments(self, comments, task_id=None):
        """分析评论情感和关键词"""
        if not comments:
            return []
            
        # 构建请求数据
        messages = [
            {
                "role": "system",
                "content": "你是一个专业的评论分析助手。请分析以下评论的情感倾向（积极、消极、中性）和关键词。"
            }
        ]
        
        # 限制一次分析的评论数量，避免超出API限制
        comments_text = [comment.content for comment in comments[:10]]
        messages.append({
            "role": "user",
            "content": f"分析以下评论：\n\n{chr(10).join([f'{i+1}. {text}' for i, text in enumerate(comments_text)])}"
        })
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        
        data = {
            'model': 'deepseek-chat',
            'messages': messages,
            'temperature': 0.1
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, data=json.dumps(data))
            response.raise_for_status()
            
            result = response.json()
            analysis = result.get('choices', [{}])[0].get('message', {}).get('content', '')
            
            # 解析分析结果
            analyzed_comments = self._parse_analysis_result(analysis, comments)
            
            # 发送分析结果到前端
            if task_id and analyzed_comments:
                socketio.emit('comments_analyzed', {
                    'task_id': task_id,
                    'comments': [comment.to_dict() for comment in analyzed_comments]
                }, room=task_id)
                
            return analyzed_comments
            
        except Exception as e:
            print(f"评论分析失败: {str(e)}")
            # 出错时将情感设为中性
            for comment in comments:
                comment.sentiment = 'neutral'
                comment.keywords = []
            return comments
    
    def _parse_analysis_result(self, analysis_text, comments):
        """解析DeepSeek API返回的分析结果"""
        # 这里需要根据DeepSeek API的实际返回格式进行解析
        # 简化版解析逻辑，实际应用中可能需要更复杂的解析
        analyzed_comments = []
        
        # 假设分析结果格式为："1. [积极] 关键词：商品,好\n2. [消极] 关键词：质量,差"
        lines = analysis_text.strip().split('\n')
        for i, line in enumerate(lines):
            if i >= len(comments):
                break
                
            try:
                # 提取情感和关键词
                sentiment_start = line.find('[') + 1
                sentiment_end = line.find(']')
                sentiment = line[sentiment_start:sentiment_end].strip()
                
                keywords_start = line.find('关键词：') + 4
                keywords_text = line[keywords_start:].strip()
                keywords = keywords_text.split(',') if keywords_text else []
                
                # 更新评论对象
                comment = comments[i]
                comment.sentiment = sentiment
                comment.keywords = keywords
                analyzed_comments.append(comment)
            except:
                # 解析失败时保持原有评论
                analyzed_comments.append(comments[i])
                
        return analyzed_comments    