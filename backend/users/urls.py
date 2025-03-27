from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('csrf/', views.get_csrf_token, name='get-csrf-token'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('verify-phone/', views.verify_phone, name='verify-phone'),
] 