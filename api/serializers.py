from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    class Meta:
        model = User
        fields = '__all__'
