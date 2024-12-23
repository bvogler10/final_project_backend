# File: models.py
# Author: Brinja Vogler (bvogler@bu.edu)
# Description: a file containing all models used in the database (and some extra for future development)

from rest_framework import serializers

from .models import Post, User, InventoryItem, Pattern, Follow
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.conf import settings



class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField() 
    class Meta:
        model = User
        fields = '__all__'

    def get_avatar(self, obj):
        if obj.avatar:
            return f"{settings.WEBSITE_URL}{obj.avatar.url}"
        return None


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

class PatternListSerializer(serializers.ModelSerializer):
    creator_info = UserSerializer(source='creator',read_only=True)
    class Meta:
        model = Pattern
        fields = [
            'id',
            'creator_info',
            'difficulty',
            'name',
            'description',
            'created_at',
            'image_url',
        ]

class InventoryListSerializer(serializers.ModelSerializer):
    user_info = UserSerializer(source='user',read_only=True)
    class Meta:
        model = InventoryItem
        fields = [
            'id',
            'image_url',
            'description',
            'item_type',
            'user_info',
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

class InventoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.UUIDField(write_only=True)

    class Meta:
        model = InventoryItem
        fields = [
            'user', 
            'name', 
            'description',
            'image',
            'item_type'
        ]

    def create(self, validated_data):
        print('validated_data:', validated_data)
        user_uuid = validated_data.pop('user')
        try:
            user = User.objects.get(id=user_uuid)
            return InventoryItem.objects.create(user=user, **validated_data)
        except User.DoesNotExist:
            raise serializers.ValidationError({"user_uuid": "Invalid user UUID."})
        
class PatternCreateSerializer(serializers.ModelSerializer):
    creator = serializers.UUIDField(write_only=True)

    class Meta:
        model = Pattern
        fields = [
            'creator', 
            'name', 
            'description',
            'image',
            'difficulty'
        ]

    def create(self, validated_data):
        print('validated_data:', validated_data)
        user_uuid = validated_data.pop('creator')
        try:
            user = User.objects.get(id=user_uuid)
            return Pattern.objects.create(creator=user, **validated_data)
        except User.DoesNotExist:
            raise serializers.ValidationError({"user_uuid": "Invalid user UUID."})
        
from rest_framework import serializers
from .models import Follow, User

class FollowCreateSerializer(serializers.ModelSerializer):
    follower = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = Follow
        fields = [
            'follower',  # Hidden and populated from request.user
            'following',  # Required field
        ]

    def create(self, validated_data):
        print('validated_data:', validated_data)
        follower = validated_data['follower']  # Current authenticated user
        following = validated_data['following']  # Provided in request data

        # Prevent self-following
        if follower == following:
            raise serializers.ValidationError({"following": "You cannot follow yourself."})

        # Ensure a duplicate follow relationship does not exist
        if Follow.objects.filter(follower=follower, following=following).exists():
            raise serializers.ValidationError({"detail": "You are already following this user."})

        return Follow.objects.create(**validated_data)
    
class FollowerListSerializer(serializers.ModelSerializer):
    follow_info = UserSerializer(source='follower',read_only=True)

    class Meta:
        model = Follow
        fields = [
            'id',
            'follow_info',
        ]
class FollowingListSerializer(serializers.ModelSerializer):
    follow_info = UserSerializer(source='following',read_only=True)

    class Meta:
        model = Follow
        fields = [
            'id',
            'follow_info',
        ]

        
