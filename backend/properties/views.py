from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status, viewsets, permissions
from .models import Property, PropertyImage, Favorite
from django.db.models import Q
from .serializers import PropertySerializer, PropertyImageSerializer, FavoriteSerializer
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as filters
from rest_framework import filters as drf_filters
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
import requests
from django.http import HttpResponse, JsonResponse
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from urllib.parse import unquote
import logging
import time
import urllib3

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger(__name__)

# Create your views here.

@api_view(['GET'])
@permission_classes([AllowAny])
def property_list(request):
    """
    房源列表视图
    支持按关键词、价格范围等条件筛选
    返回房源的基本信息列表
    """
    # 获取筛选参数
    query = request.GET.get('q', '')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    
    # 基础查询：只显示可用房源
    properties = Property.objects.filter(is_available=True)
    
    # 关键词搜索
    if query:
        properties = properties.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )
    
    # 价格范围筛选
    if min_price:
        properties = properties.filter(price__gte=min_price)
    if max_price:
        properties = properties.filter(price__lte=max_price)
    
    # 序列化数据
    serializer = PropertySerializer(properties, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def property_detail(request, pk):
    """
    房源详情视图
    返回指定房源的详细信息
    包括所有图片和收藏状态
    """
    property = get_object_or_404(Property.objects.prefetch_related('propertyimage_set'), pk=pk)
    serializer = PropertySerializer(property, context={'request': request})
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def property_create(request):
    """
    创建房源视图
    接收房源信息和图片
    创建新的房源记录
    """
    serializer = PropertySerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def property_update(request, pk):
    """
    更新房源视图
    只允许房主更新自己的房源
    支持更新基本信息和添加新图片
    """
    property = get_object_or_404(Property, pk=pk)
    serializer = PropertySerializer(property, data=request.data, partial=True, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def property_delete(request, pk):
    """
    删除房源视图
    只允许房主删除自己的房源
    """
    property = get_object_or_404(Property, pk=pk)
    property.delete()
    return Response({'message': '房源删除成功'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_favorite(request, pk):
    """
    切换收藏状态视图
    如果已收藏则取消收藏，如果未收藏则添加收藏
    """
    property = get_object_or_404(Property, pk=pk)
    favorite, created = Favorite.objects.get_or_create(user=request.user, property=property)
    
    if not created:
        favorite.delete()
        return Response({'message': '取消收藏成功'})
    
    return Response({'message': '收藏成功'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_favorites(request):
    """
    获取用户收藏列表视图
    返回用户收藏的所有房源信息
    """
    favorites = Favorite.objects.filter(user=request.user).select_related('property')
    serializer = FavoriteSerializer(favorites, many=True, context={'request': request})
    return Response(serializer.data)

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class PropertyFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    rooms = filters.CharFilter(field_name="rooms", lookup_expr='exact')
    min_area = filters.NumberFilter(field_name="areas", lookup_expr='gte')
    max_area = filters.NumberFilter(field_name="areas", lookup_expr='lte')
    
    class Meta:
        model = Property
        fields = ['min_price', 'max_price', 'rooms', 'min_area', 'max_area']

class PropertyViewSet(viewsets.ModelViewSet):
    serializer_class = PropertySerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.DjangoFilterBackend, drf_filters.SearchFilter, drf_filters.OrderingFilter]
    filterset_class = PropertyFilter
    search_fields = ['title', 'description', 'features']
    ordering_fields = ['price', 'areas', 'created_at']
    ordering = ['-created_at']
    permission_classes = [permissions.AllowAny]
    lookup_field = 'pk'

    def get_queryset(self):
        queryset = Property.objects.prefetch_related('propertyimage_set').order_by('-created_at')
        url = self.request.query_params.get('url', None)
        
        if url is not None:
            queryset = queryset.filter(url=url)
        
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        serializer.save()
    
    @action(detail=True, methods=['post', 'delete'])
    def favorite(self, request, pk=None):
        property = self.get_object()
        if request.method == 'POST':
            favorite, created = Favorite.objects.get_or_create(user=request.user, property=property)
            if not created:
                return Response({'message': '已经收藏过了'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'message': '收藏成功'})
        elif request.method == 'DELETE':
            try:
                favorite = Favorite.objects.get(user=request.user, property=property)
                favorite.delete()
                return Response({'message': '取消收藏成功'})
            except Favorite.DoesNotExist:
                return Response({'message': '未收藏该房源'}, status=status.HTTP_400_BAD_REQUEST)

class FavoriteViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Property.objects.filter(favorite__user=self.request.user)

    @action(detail=True, methods=['post'])
    def toggle(self, request, pk=None):
        property = self.get_object()
        favorite, created = Favorite.objects.get_or_create(
            user=request.user,
            property=property
        )
        if not created:
            favorite.delete()
            return Response({'message': '已取消收藏'}, status=status.HTTP_200_OK)
        return Response({'message': '已收藏'}, status=status.HTTP_201_CREATED)

@csrf_exempt
def proxy_image(request):
    """图片代理视图"""
    if request.method == 'OPTIONS':
        response = HttpResponse()
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Origin, Content-Type, Accept, Authorization'
        response['Access-Control-Max-Age'] = '86400'  # 24 hours
        return response

    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        # 获取并解码图片URL
        image_url = request.GET.get('url')
        if not image_url:
            logger.error('No URL provided in request')
            return JsonResponse({'error': 'URL parameter is required'}, status=400)

        image_url = unquote(image_url)
        logger.info(f'Proxying image from URL: {image_url}')

        # 设置请求头
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Referer': 'https://hz.lianjia.com/',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'image',
            'Sec-Fetch-Mode': 'no-cors',
            'Sec-Fetch-Site': 'cross-site',
            'Host': 'image1.ljcdn.com',
            'Origin': 'https://hz.lianjia.com',
            'Cache-Control': 'no-cache',
        }

        # 使用缓存键
        cache_key = f'proxy_image_{image_url}'
        cached_response = cache.get(cache_key)
        
        if cached_response:
            return HttpResponse(
                content=cached_response['content'],
                content_type=cached_response['content_type'],
                headers=cached_response['headers']
            )

        # 发送请求
        try:
            session = requests.Session()
            response = session.get(
                image_url,
                headers=headers,
                timeout=10,
                verify=False,
                allow_redirects=True,
                stream=True
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(f'Failed to fetch image: {str(e)}')
            return JsonResponse({'error': f'Failed to fetch image: {str(e)}'}, status=502)

        # 获取内容类型
        content_type = response.headers.get('Content-Type', 'image/jpeg')
        
        # 读取响应内容
        content = b''
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                content += chunk

        # 设置响应头
        response_headers = {
            'Content-Type': content_type,
            'Content-Length': len(content),
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, OPTIONS',
            'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization',
            'Cache-Control': 'public, max-age=31536000',
            'X-Frame-Options': 'SAMEORIGIN',
            'X-Content-Type-Options': 'nosniff',
        }

        # 缓存响应
        cache.set(cache_key, {
            'content': content,
            'content_type': content_type,
            'headers': response_headers
        }, timeout=86400)  # 24小时缓存

        # 返回图片数据
        return HttpResponse(
            content=content,
            status=200,
            headers=response_headers
        )

    except Exception as e:
        logger.exception('Unexpected error in proxy_image view')
        return JsonResponse({
            'error': 'Internal server error',
            'detail': str(e)
        }, status=500)
