import sys
sys.path.append('../../')
from utils.api import get_user_and_token_by_jwt_request
from rest_framework.permissions import BasePermission
from .models import UserType


class IsAdminUserPermission(BasePermission):
    def has_permission(self, request, view):
        user, token = get_user_and_token_by_jwt_request(request)
        return (user.user_type == UserType.ADMIN_USER)