from rest_framework import serializers

from .models import Post, User, InventoryItem
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
        
class InventoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = [
            'id',
            'image_url',
            'description',
            'item_type',
            'name',
        ]

class PostCreateSerializer(serializers.ModelSerializer):
    user = serializers.UUIDField(write_only=True)

    class Meta:
        model = Post
        fields = [
            'user', 
            'image', 
            'caption',
        ]

    def create(self, validated_data):
        print('validated_data:', validated_data)
        user_uuid = validated_data.pop('user')
        try:
            user = User.objects.get(id=user_uuid)
            print("user:", user)
            # user_info = UserSerializer(source=user,read_only=True)
            return Post.objects.create(user=user, **validated_data)
        except User.DoesNotExist:
            raise serializers.ValidationError({"user_uuid": "Invalid user UUID."})
        
        
