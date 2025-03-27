from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from users.models import User
from .models import ChatMessage

class ChatAPITests(TestCase):
    def setUp(self):
        """测试前的准备工作"""
        # 创建测试用户
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # 创建测试消息
        self.message = ChatMessage.objects.create(
            user=self.user,
            content='测试消息'
        )
        
        # 设置API客户端
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        # 设置测试URL
        self.list_url = reverse('chat-message-list')
        self.detail_url = reverse('chat-message-detail', kwargs={'pk': self.message.message_id})

    def test_send_message(self):
        """测试发送消息"""
        data = {
            'content': '你好，我想咨询一下房源信息'
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ChatMessage.objects.count(), 2)  # 用户消息和AI回复

    def test_get_message_list(self):
        """测试获取消息列表"""
        # 先创建一些测试消息
        ChatMessage.objects.create(
            user=self.user,
            content='测试消息1',
            is_bot=False
        )
        ChatMessage.objects.create(
            user=self.user,
            content='测试消息2',
            is_bot=True
        )
        
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['results']) >= 3)  # 包括setUp中创建的消息
        self.assertTrue(any(m['content'] == '测试消息' for m in response.data['results']))
        self.assertTrue(any(m['content'] == '测试消息1' for m in response.data['results']))
        self.assertTrue(any(m['content'] == '测试消息2' for m in response.data['results']))

    def test_get_message_detail(self):
        """测试获取消息详情"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], '测试消息')

    def test_delete_message(self):
        """测试删除消息"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ChatMessage.objects.count(), 0)
