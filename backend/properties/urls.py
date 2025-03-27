from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'properties'

router = DefaultRouter()
router.register(r'properties', views.PropertyViewSet, basename='property')
router.register(r'favorites', views.FavoriteViewSet, basename='favorite')

urlpatterns = [
    path('proxy-image/', views.proxy_image, name='proxy-image'),
    path('', include(router.urls)),
] 