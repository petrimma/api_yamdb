from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'bio',
            'email',
            'role',
        ]


class SendCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class UserTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, write_only=True)
    confirmation_code = serializers.CharField(required=True, write_only=True)
