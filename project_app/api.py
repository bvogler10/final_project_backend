from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from django.shortcuts import get_object_or_404


from .models import Post, InventoryItem, User, Pattern
from .serializers import PostListSerializer, PostCreateSerializer, UserSerializer, InventoryListSerializer, UserPartialUpdateSerializer, InventoryCreateSerializer, PatternListSerializer

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
@authentication_classes([JWTAuthentication])
@permission_classes([])
def get_all_but_user_posts(request):
    user = request.user
    posts = Post.objects.exclude(user=user).order_by('-created_at')
    serializer = PostListSerializer(posts, many=True)
    return JsonResponse({
        'data': serializer.data
    })

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def get_all_patterns(request):
    posts = Pattern.objects.all().order_by('-created_at')
    serializer = PatternListSerializer(posts, many=True)
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
    items = InventoryItem.objects.filter(user=user_id).order_by('created_at', 'item_type')
    serializer = InventoryListSerializer(items, many=True)
    return JsonResponse({
        'data': serializer.data
    })

@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([])
def update_user(request):
    user = request.user
    print('PUT REQUEST', user, flush=True)

    if not user.is_authenticated:
        return JsonResponse({"error": "you must be authenticated to perform this"})
    
    avatar = request.FILES.get('avatar')
    link = request.data.get('link')
    bio = request.data.get('bio')
    
    # Update the profile picture if it was provided
    if avatar:
        user.avatar = avatar   
    user.bio = bio
    user.link = link

    user.save()
    serializer = UserSerializer(user)
    return JsonResponse({'data': serializer.data})

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([])
def create_post(request):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({"error": "you must be authenticated to perform this"})
    
    serializer = PostCreateSerializer(data=request.data)
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

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([])
def create_inventory_item(request, user_id):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({"error": "you must be authenticated to perform this"})
    
    serializer = InventoryCreateSerializer(data=request.data)
    if serializer.is_valid():
        post = serializer.save()
        print(post)
        return JsonResponse({
            "message": "Post created successfully!",
        }, status=status.HTTP_201_CREATED)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)