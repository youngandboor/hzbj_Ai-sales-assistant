from rest_framework import serializers
from .models import ChatMessage
from users.serializers import UserSerializer

class ChatMessageSerializer(serializers.ModelSerializer):
    """聊天消息序列化器"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = ChatMessage
        fields = ['message_id', 'user', 'is_bot', 'content', 'created_at']
        read_only_fields = ['message_id', 'created_at'] 