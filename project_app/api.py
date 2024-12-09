from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Q


from .models import Post, InventoryItem, User, Pattern, Follow
from .serializers import PostListSerializer, PostCreateSerializer, UserSerializer, InventoryListSerializer, InventoryCreateSerializer, PatternListSerializer, PatternCreateSerializer, FollowCreateSerializer, FollowerListSerializer, FollowingListSerializer

#------POST GET VIEWS-------
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
@authentication_classes([JWTAuthentication])
@permission_classes([])
def get_following_posts(request):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({"error": "Authentication is required"}, status=401)
    
    # Filter posts based on the following relationships
    following_users = Follow.objects.filter(follower=user).values_list('following', flat=True)
    posts = Post.objects.filter(user__in=following_users).order_by('-created_at')
    
    serializer = PostListSerializer(posts, many=True)
    return JsonResponse({
        'data': serializer.data
    })

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([])
def get_explore_posts(request):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({"error": "Authentication is required"}, status=401)
    
    # Filter posts based on the following relationships
    following_users = Follow.objects.filter(follower=user).values_list('following', flat=True)
    
    # Exclude the posts by the current user and the users that the user is following
    posts = Post.objects.exclude(user=user)  # Exclude posts from the user
    posts = posts.exclude(user__in=following_users)  # Exclude posts from users that the current user is following
    posts = posts.order_by('-created_at')
    
    serializer = PostListSerializer(posts, many=True)
    return JsonResponse({
        'data': serializer.data
    })

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



#-----PATTERN GET VIEWS-------
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
@authentication_classes([JWTAuthentication])
@permission_classes([])
def get_all_but_user_patterns(request):
    user = request.user
    posts = Post.objects.exclude(user=user).order_by('-created_at')
    serializer = PostListSerializer(posts, many=True)
    return JsonResponse({
        'data': serializer.data
    })

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([])
def get_following_patterns(request):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({"error": "Authentication is required"}, status=401)
    
    following_users = Follow.objects.filter(follower=user).values_list('following', flat=True)
    patterns = Pattern.objects.filter(creator__in=following_users).order_by('-created_at')

    serializer = PatternListSerializer(patterns, many=True)
    return JsonResponse({
        'data': serializer.data
    })

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([])
def get_explore_patterns(request):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({"error": "Authentication is required"}, status=401)
    
    # Filter patterns based on the following relationships
    following_users = Follow.objects.filter(follower=user).values_list('following', flat=True)
    
    # Exclude the patterns by the current user and the users that the user is following
    patterns = Pattern.objects.exclude(creator=user)  # Exclude patterns from the user
    patterns = patterns.exclude(creator__in=following_users)  # Exclude patterns from users that the current user is following
    patterns = patterns.order_by('-created_at')
    
    serializer = PatternListSerializer(patterns, many=True)
    return JsonResponse({
        'data': serializer.data
    })

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([])
def create_pattern(request, user_id):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({"error": "you must be authenticated to perform this"})
    
    serializer = PatternCreateSerializer(data=request.data)
    if serializer.is_valid():
        post = serializer.save()
        print(post)
        return JsonResponse({
            "message": "Pattern created successfully!",
        }, status=status.HTTP_201_CREATED)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([]) 
def get_patterns_with_search(request):
    user = request.user 
    if not user.is_authenticated:
        return JsonResponse({"error": "you must be authenticated to perform this"})
    
    search_query = request.GET.get('search_query', None)
    # Start with all patterns
    patterns = Pattern.objects.all()
    # Exclude user's own patterns
    patterns = patterns.exclude(creator=user)
    
    if search_query:
        patterns = patterns.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )

    # Order by difficulty
    patterns = patterns.order_by('difficulty')
    
    serializer = PatternListSerializer(patterns, many=True)
    return JsonResponse({'data': serializer.data})

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def get_pattern_by_id(request, pattern_id):
    pattern = get_object_or_404(Pattern, id=pattern_id)
    serializer = PatternListSerializer(pattern)
    return JsonResponse({
        'data': serializer.data
    })



#-------USER VIEWS---------
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
def get_user_posts(request, user_id):
    posts = Post.objects.filter(user=user_id).order_by('-created_at')
    serializer = PostListSerializer(posts, many=True)
    return JsonResponse({
        'data': serializer.data
    })

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def get_user_patterns(request, user_id):
    patterns = Pattern.objects.filter(creator=user_id).order_by('-created_at')
    serializer = PatternListSerializer(patterns, many=True)
    return JsonResponse({
        'data': serializer.data
    })

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def get_user_followers(request, user_id):
    
    follows = Follow.objects.filter(following=user_id)
    serializer = FollowerListSerializer(follows, many=True)
    return JsonResponse({
        'data': serializer.data
    })

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def get_user_following(request, user_id):
    follows = Follow.objects.filter(follower=user_id)
    serializer = FollowingListSerializer(follows, many=True)
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
def create_follow(request, other_id):
    user = request.user
    print(user)
    if not user.is_authenticated:
        return JsonResponse({"error": "You must be authenticated to perform this"}, status=status.HTTP_401_UNAUTHORIZED)
    
    # Ensure the other user exists
    try:
        other_user = User.objects.get(id=other_id)
    except User.DoesNotExist:
        return JsonResponse({"error": "User to follow does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    # Pass data to serializer
    data = {'following': other_id}
    serializer = FollowCreateSerializer(data=data, context={'request': request})
    
    if serializer.is_valid():
        follow = serializer.save()  # Save the follow instance
        return JsonResponse({
            "message": "Successfully followed!",
            "follow_id": str(follow.id),  # Optionally return the follow ID
        }, status=status.HTTP_201_CREATED)
    
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([]) 
def search_users(request):
    user = request.user 
    if not user.is_authenticated:
        return JsonResponse({"error": "you must be authenticated to perform this"})
    
    search_query = request.GET.get('search_query', None)
    # Start with all patterns
    users = User.objects.all()
    # Exclude self
    users = users.exclude(id=user.id)
    
    if search_query:
        users = users.filter(
            Q(name__icontains=search_query) | Q(username__icontains=search_query)
        )
    
    serializer = UserSerializer(users, many=True)
    return JsonResponse({'data': serializer.data})



#--------INVENTORY VIEWS-------
@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def get_inventory(request, user_id):
    items = InventoryItem.objects.filter(user=user_id).order_by('created_at', 'item_type')
    serializer = InventoryListSerializer(items, many=True)
    return JsonResponse({
        'data': serializer.data
    })

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
            "message": "Item created successfully!",
        }, status=status.HTTP_201_CREATED)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([])
def delete_inventory_item(request, inventory_id):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({"error": "you must be authenticated to perform this"})
    
    item = get_object_or_404(InventoryItem, id=inventory_id)
    item.delete()
    return JsonResponse({"message": "item successfully deleted"})