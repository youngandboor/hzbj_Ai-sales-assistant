from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, viewsets, permissions
from rest_framework.pagination import PageNumberPagination
from .models import ChatMessage
from .serializers import ChatMessageSerializer
from properties.permissions import IsOwnerOrReadOnly

class ChatMessagePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class ChatMessageViewSet(viewsets.ModelViewSet):
    """
    聊天消息视图集
    提供消息的增删改查功能
    """
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = ChatMessagePagination
    ordering = ['-created_at']
    
    def get_queryset(self):
        """获取当前用户的所有聊天消息"""
        return ChatMessage.objects.filter(user=self.request.user).order_by('-created_at')
    
    def perform_create(self, serializer):
        """创建新消息时自动设置用户"""
        serializer.save(user=self.request.user)
    
    def list(self, request, *args, **kwargs):
        """重写列表方法，返回分页数据"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request):
    """
    发送消息视图
    保存用户消息并生成AI回复
    返回发送成功信息和AI回复
    """
    content = request.data.get('content')
    
    if not content:
        return Response({'error': '消息内容不能为空'}, status=status.HTTP_400_BAD_REQUEST)
    
    # 保存用户消息
    user_message = ChatMessage.objects.create(
        user=request.user,
        content=content,
        is_bot=False
    )
    
    # 这里应该调用AI服务生成回复
    # 示例回复
    ai_response = "感谢您的咨询。我是AI助手，我会尽力回答您的问题。"
    
    # 保存AI回复
    ai_message = ChatMessage.objects.create(
        user=request.user,
        content=ai_response,
        is_bot=True
    )
    
    return Response({
        'message': '消息发送成功',
        'ai_response': {
            'content': ai_message.content,
            'created_at': ai_message.created_at
        }
    })
