from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import User, UserProfile

class UserAPITests(TestCase):
    def setUp(self):
        """测试前的准备工作"""
        # 创建测试用户
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            phone='13800138000'
        )
        
        # 设置API客户端
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        # 设置测试URL
        self.register_url = reverse('users:register')
        self.login_url = reverse('users:login')
        self.logout_url = reverse('users:logout')
        self.profile_url = reverse('users:profile')
        self.verify_phone_url = reverse('users:verify-phone')

    def test_user_registration(self):
        """测试用户注册"""
        data = {
            'username': 'newuser',
            'password': 'newpass123',
            'email': 'new@example.com',
            'phone': '13800138001'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)  # 包括setUp中创建的用户

    def test_user_login(self):
        """测试用户登录"""
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_logout(self):
        """测试用户退出"""
        # 先登录
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_profile(self):
        """测试获取用户资料"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')

    def test_update_profile(self):
        """测试更新用户资料"""
        self.client.login(username='testuser', password='testpass123')
        data = {
            'real_name': '测试用户',
            'bio': '这是一个测试用户'
        }
        response = self.client.patch(self.profile_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_verify_phone(self):
        """测试手机号验证"""
        self.client.login(username='testuser', password='testpass123')
        data = {'code': '1234'}  # 使用测试验证码
        response = self.client.post(self.verify_phone_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_verified)
