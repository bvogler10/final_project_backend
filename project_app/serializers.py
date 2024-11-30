from rest_framework import serializers

from .models import Post, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class PostListSerializer(serializers.ModelSerializer):
    user_info = UserSerializer(source='user',read_only=True)
    class Meta:
        model = Post
        fields = [
            'user_info',
            'image_url',
            'created_at',
            'caption',
            'pattern',
        ]