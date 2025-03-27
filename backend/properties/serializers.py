from rest_framework import serializers
from .models import Property, PropertyImage, Favorite
from users.serializers import UserSerializer

class PropertyImageSerializer(serializers.ModelSerializer):
    """房源图片序列化器"""
    class Meta:
        model = PropertyImage
        fields = ['id', 'image', 'is_main']
        read_only_fields = ['id']

class PropertySerializer(serializers.ModelSerializer):
    """房源序列化器"""
    images = PropertyImageSerializer(many=True, read_only=True, source='propertyimage_set')
    is_favorited = serializers.SerializerMethodField()
    
    class Meta:
        model = Property
        fields = ['id', 'title', 'description',
                 'price', 'perprice', 'rooms', 'areas', 'direction', 'zhuangXiu',
                 'floor', 'Structure', 'features', 'url', 'is_available',
                 'images', 'is_favorited', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_is_favorited(self, obj):
        """获取当前用户是否收藏了该房源"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Favorite.objects.filter(user=request.user, property=obj).exists()
        return False

class FavoriteSerializer(serializers.ModelSerializer):
    """收藏序列化器"""
    property = PropertySerializer(read_only=True)
    
    class Meta:
        model = Favorite
        fields = ['id', 'property', 'created_at']
        read_only_fields = ['id', 'created_at'] 