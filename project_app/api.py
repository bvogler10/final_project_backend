from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from django.shortcuts import get_object_or_404


from .models import Post, InventoryItem, User
from .serializers import PostListSerializer, PostCreateSerializer, UserSerializer, InventoryListSerializer

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def get_all_posts(request):
    posts = Post.objects.all().order_by('-created_at')
    serializer = PostListSerializer(posts, many=True)
    return JsonResponse({
        'data': serializer.data
    })

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def get_user_posts(request, user_id):
    posts = Post.objects.filter(user=user_id).order_by('-created_at')
    serializer = PostListSerializer(posts, many=True)
    return JsonResponse({
        'data': serializer.data
    })

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def get_user_by_id(request, user_id):
    user = get_object_or_404(User, id=user_id)
    serializer = UserSerializer(user)
    return JsonResponse({
        'data': serializer.data
    })

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def get_inventory(request, user_id):
    items = InventoryItem.objects.filter(user=user_id).order_by('item_type')
    serializer = InventoryListSerializer(items, many=True)
    return JsonResponse({
        'data': serializer.data
    })

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([])
def create_post(request):
    print(request.data)

    serializer = PostCreateSerializer(data=request.data)
    print('serializer:', serializer)
    if serializer.is_valid():
        post = serializer.save()
        print(post)
        return JsonResponse({
            "message": "Post created successfully!",
            "post": {
                "id": str(post.id),
                "image": post.image_url() if post.image else "",
                "pattern": post.pattern,
                "caption": post.caption,
                "created_at": post.created_at
            }
        }, status=status.HTTP_201_CREATED)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)