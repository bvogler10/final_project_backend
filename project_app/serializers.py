from rest_framework import serializers

from .models import Post, User
from dj_rest_auth.registration.serializers import RegisterSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CustomRegisterSerializer(RegisterSerializer):
    name = serializers.CharField(max_length=100)
    username = serializers.CharField(max_length=100)

    def custom_signup(self, request, user):
        # Set the username field explicitly during signup
        user.name = self.validated_data.get('name', '')
        user.username = self.validated_data.get('username', '')
        user.save(update_fields=['name', 'username'])

class PostListSerializer(serializers.ModelSerializer):
    user_info = UserSerializer(source='user',read_only=True)
    class Meta:
        model = Post
        fields = [
            'id',
            'user_info',
            'image_url',
            'created_at',
            'caption',
            'pattern',
        ]