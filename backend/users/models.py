from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password, phone, **extra_fields):
        if not username:
            raise ValueError('用户名是必填项')
        if not phone:
            raise ValueError('手机号是必填项')
            
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_verified', False)
        extra_fields.setdefault('member_level', 'normal')
        
        user = self.model(
            username=username,
            phone=phone,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user
        
    def create_superuser(self, username, password, phone, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        return self.create_user(username, password, phone, **extra_fields)

class User(AbstractUser):
    """自定义用户模型"""
    # 移除first_name和last_name字段
    first_name = None
    last_name = None
    
    # 数据库中的字段,完全按照数据库表结构
    id = models.BigAutoField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(max_length=150, unique=True, verbose_name='用户名')
    email = models.EmailField(blank=True, verbose_name='邮箱')
    is_staff = models.BooleanField(default=False, verbose_name='是否为员工')
    is_active = models.BooleanField(default=True, verbose_name='是否激活')
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='加入时间')
    phone = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    is_verified = models.BooleanField()
    avatar_url = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    house_intention = models.CharField(max_length=10, null=True)
    member_level = models.CharField(max_length=10)
    preferred_area = models.CharField(max_length=50, null=True)
    real_name = models.CharField(max_length=50, null=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    verification_code = models.CharField(max_length=6, null=True)
    verification_code_expires = models.DateTimeField(null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone']

    class Meta:
        db_table = 'users'
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __str__(self):
        return self.username

class UserProfile(models.Model):
    """用户资料模型"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', db_column='user_id')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='头像')
    bio = models.TextField(verbose_name='个人简介')

    class Meta:
        db_table = 'users_userprofile'
        verbose_name = '用户资料'
        verbose_name_plural = '用户资料'

    def __str__(self):
        return f"{self.user.username}的资料"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, bio='')

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=instance, bio='')
