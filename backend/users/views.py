from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status, viewsets, permissions
from .models import User, UserProfile
from .serializers import UserSerializer, UserProfileSerializer
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.views import View

User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    用户注册视图
    接收用户名、密码和手机号码
    创建新用户和对应的用户资料
    返回注册成功或失败信息
    """
    print("收到注册请求")
    print("请求数据:", request.data)
    print("请求方法:", request.method)
    print("请求头:", request.headers)
    
    username = request.data.get('username')
    password = request.data.get('password')
    phone = request.data.get('phone')
    email = request.data.get('email')  # 可选字段
    
    print("提取的字段:")
    print("username:", username)
    print("password:", password)
    print("phone:", phone)
    print("email:", email)
    
    # 检查必填字段
    if not all([username, password, phone]):
        error_msg = '用户名、密码和手机号都是必填项'
        print("错误:", error_msg)
        print("缺失字段:", [k for k, v in {'username': username, 'password': password, 'phone': phone}.items() if not v])
        return Response({'error': error_msg}, status=status.HTTP_400_BAD_REQUEST)
    
    # 检查用户名是否已存在
    if User.objects.filter(username=username).exists():
        error_msg = '用户名已存在'
        print("错误:", error_msg)
        return Response({'error': error_msg}, status=status.HTTP_400_BAD_REQUEST)
    
    # 检查手机号是否已存在
    if User.objects.filter(phone=phone).exists():
        error_msg = '手机号已被注册'
        print("错误:", error_msg)
        return Response({'error': error_msg}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # 创建新用户（用户资料会通过信号自动创建）
        user = User.objects.create_user(
            username=username,
            password=password,
            phone=phone,
            email=email or '',  # 如果没有提供email，则使用空字符串
            is_verified=False
        )
        
        print("用户创建成功:", user.username)
        return Response({
            'message': '注册成功',
            'user': {
                'id': user.id,
                'username': user.username,
                'phone': user.phone,
                'email': user.email
            }
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        error_msg = f'注册失败: {str(e)}'
        print("错误:", error_msg)
        print("错误类型:", type(e))
        import traceback
        print("错误堆栈:", traceback.format_exc())
        return Response({'error': error_msg}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    用户登录视图
    接收用户名和密码
    验证用户身份并创建会话
    返回登录成功或失败信息
    """
    print("收到登录请求")
    print("请求数据:", request.data)
    print("请求方法:", request.method)
    print("请求头:", request.headers)
    
    username = request.data.get('username')
    password = request.data.get('password')
    
    print("提取的字段:")
    print("username:", username)
    print("password:", password)
    
    # 验证用户身份
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        print("登录成功")
        return Response({'message': '登录成功'})
    print("登录失败: 用户名或密码错误")
    return Response({'error': '用户名或密码错误'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    用户退出视图
    清除用户会话
    返回退出成功信息
    """
    logout(request)
    return Response({'message': '退出成功'})

@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def profile(request):
    """
    用户资料视图
    GET: 获取用户资料信息
    PUT/PATCH: 更新用户资料信息
    包括头像和个人简介
    """
    if request.method == 'GET':
        # 获取用户资料
        user = request.user
        data = {
            'username': user.username,
            'phone': user.phone,
            'email': user.email,
            'is_verified': user.is_verified,
            'avatar_url': user.avatar_url,
            'member_level': user.member_level,
            'house_intention': user.house_intention,
            'preferred_area': user.preferred_area,
            'avatar': user.profile.avatar.url if user.profile.avatar else None,
            'bio': user.profile.bio
        }
        return Response(data)
    
    elif request.method in ['PUT', 'PATCH']:
        # 更新用户资料
        user = request.user
        profile = user.profile
        
        if 'bio' in request.data:
            profile.bio = request.data['bio']
        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']
            
        profile.save()
        return Response({'message': '个人资料更新成功'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_phone(request):
    """
    手机验证视图
    接收验证码并验证
    更新用户的验证状态
    返回验证成功或失败信息
    """
    code = request.data.get('code')
    # 这里应该添加验证码验证逻辑
    if code == '1234':  # 示例验证码
        request.user.is_verified = True
        request.user.save()
        return Response({'message': '手机验证成功'})
    return Response({'error': '验证码错误'}, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        if self.action == 'list':
            return User.objects.filter(id=self.request.user.id)
        return super().get_queryset()
    
    @action(detail=False, methods=['get', 'put'])
    def profile(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = UserProfileSerializer(user.profile)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = UserProfileSerializer(user.profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def get_csrf_token(request):
    """
    获取CSRF token的视图
    返回CSRF token
    """
    return Response({'csrfToken': get_token(request)})
