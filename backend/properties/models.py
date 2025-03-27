from django.db import models
from users.models import User
from django.utils import timezone

class Property(models.Model):
    """房源模型"""
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=200, default='', verbose_name='标题')
    description = models.TextField(default='', verbose_name='描述')
    price = models.IntegerField(default=0, verbose_name='总价')
    perprice = models.IntegerField(default=0, verbose_name='单价')
    rooms = models.CharField(max_length=20, default='0', verbose_name='房间数')
    areas = models.CharField(max_length=20, default='0', verbose_name='面积')
    direction = models.CharField(max_length=255, default='未知', verbose_name='朝向')
    zhuangXiu = models.CharField(max_length=255, null=True, blank=True, verbose_name='装修')
    floor = models.CharField(max_length=20, default='未知', verbose_name='楼层')
    Structure = models.CharField(max_length=50, default='未知', verbose_name='结构')
    features = models.CharField(max_length=255, default='', verbose_name='特点')
    url = models.CharField(max_length=255, default='', verbose_name='链接')
    created_at = models.DateTimeField(null=True, blank=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(null=True, blank=True, verbose_name='更新时间')
    is_available = models.BooleanField(default=True, verbose_name='是否可用')

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'properties'
        verbose_name = '房源'
        verbose_name_plural = '房源'

    def __str__(self):
        return self.title

    @property
    def images(self):
        """获取房源的所有图片"""
        return self.propertyimage_set.all()

class PropertyImage(models.Model):
    """房源图片模型"""
    id = models.BigAutoField(primary_key=True)
    image = models.CharField(max_length=100, verbose_name='图片URL')
    is_main = models.BooleanField(default=True, verbose_name='是否主图')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, db_column='property_id', verbose_name='所属房源')

    class Meta:
        db_table = 'property_images'
        verbose_name = '房源图片'
        verbose_name_plural = '房源图片'

    def __str__(self):
        return f"{self.property.title} - 图片 {self.id}"

class Favorite(models.Model):
    """收藏模型"""
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, db_column='property_id')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'favorites'
        verbose_name = '收藏'
        verbose_name_plural = '收藏'
        unique_together = ('user', 'property')

    def __str__(self):
        return f"{self.user.username} 收藏了 {self.property.title}"
