from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    自定义权限类
    只允许管理员进行修改操作，其他用户只能查看
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    自定义权限类
    只允许对象的所有者进行修改操作，其他用户只能查看
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user 