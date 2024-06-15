from rest_framework.permissions import BasePermission

from redis_service.utils import RedisStore


class IsNotBlocked(BasePermission):
    """
    Custom permission to check if the user is not blocked.
    """

    def has_permission(self, request, view):
        # Ensure user is authenticated
        if not request.user or not request.user.is_authenticated:
            return False

        user_id = request.user.id
        blocked_key = f'blocked:{user_id}'

        # Check if the user ID exists in Redis as a blocked key
        if RedisStore().get(key=blocked_key):
            return False

        return True
