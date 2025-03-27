from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from users.models import User
from properties.models import Property, PropertyImage, Favorite
from chat.models import ChatMessage

class UserAPITests(APITestCase):
    def setUp(self):
        # 创建测试用户
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com',
            phone='13800138000'
        )
        
        # 创建API客户端
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        # 设置URL
        self.register_url = reverse('user-list')
        self.profile_url = reverse('user-profile')
    
    def test_user_registration(self):
        """测试用户注册API"""
        data = {
            'username': 'newuser',
            'password': 'newpass123',
            'email': 'new@example.com',
            'phone': '13900139000'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)  # 包括测试用户
    
    def test_get_user_profile(self):
        """测试获取用户资料API"""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['phone'], '13800138000')

class PropertyAPITests(APITestCase):
    def setUp(self):
        # 创建测试用户
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # 创建测试房源
        self.property = Property.objects.create(
            title='测试房源',
            description='这是一个测试房源',
            price=1000000,
            per_price=20000,
            rooms='3室2厅',
            area='100平米',
            page_url='http://example.com/property/1'
        )
        
        # 创建API客户端
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        # 设置URL
        self.property_list_url = reverse('property-list')
        self.property_detail_url = reverse('property-detail', kwargs={'pk': self.property.property_id})
    
    def test_get_property_list(self):
        """测试获取房源列表API"""
        response = self.client.get(self.property_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_get_property_detail(self):
        """测试获取房源详情API"""
        response = self.client.get(self.property_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], '测试房源')
    
    def test_create_property(self):
        """测试创建房源API"""
        data = {
            'title': '新房源',
            'description': '这是一个新房源',
            'price': 2000000,
            'per_price': 25000,
            'rooms': '4室2厅',
            'area': '150平米',
            'page_url': 'http://example.com/property/2'
        }
        response = self.client.post(self.property_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Property.objects.count(), 2)

class ChatAPITests(APITestCase):
    def setUp(self):
        # 创建测试用户
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # 创建测试消息
        self.chat_message = ChatMessage.objects.create(
            user=self.user,
            content='测试消息',
            is_bot=False
        )
        
        # 创建API客户端
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        # 设置URL
        self.chat_list_url = reverse('chat-message-list')
    
    def test_get_chat_messages(self):
        """测试获取聊天消息列表API"""
        response = self.client.get(self.chat_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_create_chat_message(self):
        """测试创建聊天消息API"""
        data = {
            'content': '新消息',
            'is_bot': False
        }
        response = self.client.post(self.chat_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ChatMessage.objects.count(), 2) 