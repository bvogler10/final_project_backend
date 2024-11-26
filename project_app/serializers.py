from rest_framework import serializers

from .models import Post

class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'user',
            'image_url',
            'pattern',
            'caption',
            'created_at',
        )