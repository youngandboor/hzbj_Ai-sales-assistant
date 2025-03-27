from django.db import models
from django.conf import settings
from users.models import User

class ChatMessage(models.Model):
    """聊天消息模型"""
    message_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    is_bot = models.BooleanField(default=False)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'chat_messages'
        verbose_name = '聊天消息'
        verbose_name_plural = '聊天消息'
        ordering = ['created_at']

    def __str__(self):
        return f"{self.user.username} - {'机器人' if self.is_bot else '用户'}消息"
