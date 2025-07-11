import requests
import json
import os
import time
from app.extensions import socketio
from app.config import config

class VoiceService:
    def __init__(self):
        self.api_key = config['BAIDU_API_KEY']
        self.secret_key = config['BAIDU_SECRET_KEY']
        self.api_url = config['BAIDU_TTS_URL']
        self.token = None
        self.token_expires_at = 0
        
    def get_access_token(self):
        """获取百度API访问令牌"""
        now = int(time.time())
        if self.token and self.token_expires_at > now + 60:
            return self.token
            
        # 请求新令牌
        auth_url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={self.api_key}&client_secret={self.secret_key}"
        response = requests.get(auth_url)
        
        if response.status_code != 200:
            raise Exception(f"获取访问令牌失败: {response.text}")
            
        result = response.json()
        self.token = result.get('access_token')
        self.token_expires_at = now + result.get('expires_in', 0)
        return self.token
    
    def generate_voice(self, text, task_id, user_id):
        """生成语音文件"""
        try:
            token = self.get_access_token()
            tts_url = f"{self.api_url}?access_token={token}"
            
            data = {
                "tex": text,
                "tok": token,
                "cuid": f"user_{user_id}",
                "ctp": 1,
                "lan": "zh",  # 中文
                "per": 4  # 发音人选择
            }
            
            response = requests.post(tts_url, data=data)
            
            if response.headers.get('Content-Type') == 'application/json':
                # 错误响应
                error = response.json()
                raise Exception(f"语音合成失败: {error.get('err_msg', '未知错误')}")
                
            # 保存语音文件
            voice_dir = os.path.join(config['VOICE_FILES_DIR'], str(task_id))
            os.makedirs(voice_dir, exist_ok=True)
            
            timestamp = int(time.time())
            file_path = os.path.join(voice_dir, f"{timestamp}.mp3")
            
            with open(file_path, 'wb') as f:
                f.write(response.content)
                
            # 构建可访问的URL
            file_url = f"/api/voices/{task_id}/{timestamp}.mp3"
            
            # 通知前端语音已生成
            socketio.emit('voice_generated', {
                'task_id': task_id,
                'text': text,
                'voice_url': file_url
            }, room=task_id)
            
            return file_url
            
        except Exception as e:
            print(f"语音合成错误: {str(e)}")
            return None    