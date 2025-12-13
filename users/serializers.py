# users/serializers.py

from djoser.serializers import (
    UserCreateSerializer as BaseUserCreateSerializer,
    UserSerializer as BaseUserSerializer
)
from django.contrib.auth import get_user_model

User = get_user_model()


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'phone_number']


class UserSerializer(BaseUserSerializer):   # ✅ FIXED NAME
    class Meta(BaseUserSerializer.Meta):
        ref_name = 'CustomUser'
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'is_staff',
            'is_superuser',
            'is_active',
        ]
