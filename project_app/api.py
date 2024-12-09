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
    '''a function to get all posts for all  users'''
    # order by most recent first, then serialize and send back
    posts = Post.objects.all().order_by('-created_at')
    serializer = PostListSerializer(posts, many=True)
    return JsonResponse({
        'data': serializer.data
    })

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([])
def get_all_but_user_posts(request):
    '''a function to get all posts except the authenticated user's'''
    # get the user from the request 
    user = request.user
    # fetch posts but exclude the posts by the user, then serialize and send back
    posts = Post.objects.exclude(user=user).order_by('-created_at')
    serializer = PostListSerializer(posts, many=True)
    return JsonResponse({
        'data': serializer.data
    })

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([])
def get_following_posts(request):
    '''a function to get all posts by users the current user follows'''
    user = request.user
    # check for authentication
    if not user.is_authenticated:
        return JsonResponse({"error": "Authentication is required"}, status=401)
    
    # Filter posts by fetching following and retrieving only posts by users in the following list
    following_users = Follow.objects.filter(follower=user).values_list('following', flat=True)
    posts = Post.objects.filter(Q(user__in=following_users) | Q(user=user)).order_by('-created_at')
    
    #serialize and send response
    serializer = PostListSerializer(posts, many=True)
    return JsonResponse({
        'data': serializer.data
    })

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([])
def get_explore_posts(request):
    '''a function to get posts for the explore page for current user'''
    user = request.user
    # check for authentication
    if not user.is_authenticated:
        return JsonResponse({"error": "Authentication is required"}, status=401)
    
    # filter posts based on the following relationships
    following_users = Follow.objects.filter(follower=user).values_list('following', flat=True)
    
    # exclude the posts by the current user and the users that the user is following
    posts = Post.objects.exclude(user=user) 
    posts = posts.exclude(user__in=following_users)
    posts = posts.order_by('-created_at')
    
    # serialize and send response
    serializer = PostListSerializer(posts, many=True)
    return JsonResponse({
        'data': serializer.data
    })

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([])
def create_post(request):
    '''a function to create a post for an authenticated user'''
    user = request.user
    # check for authentication
    if not user.is_authenticated:
        return JsonResponse({"error": "you must be authenticated to perform this"})
    # serialize the data using the post creation serializer
    serializer = PostCreateSerializer(data=request.data)
    # check if serilaized correctly and save, then send back post information
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
    # otherwise send error response
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#-----PATTERN GET VIEWS-------
@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def get_all_patterns(request):
    '''a function to get all patterns from the database'''
    # sort by most recent
    patterns = Pattern.objects.all().order_by('-created_at')

    # serialize the patterns and respond with the pattern list
    serializer = PatternListSerializer(patterns, many=True)
    return JsonResponse({
        'data': serializer.data
    })

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([])
def get_all_but_user_patterns(request):
    '''a function to get all patterns but ones created by the authenticated user'''
    user = request.user
    # exclude the current user, serialize and send back
    posts = Post.objects.exclude(user=user).order_by('-created_at')
    serializer = PostListSerializer(posts, many=True)
    return JsonResponse({
        'data': serializer.data
    })

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([])
def get_following_patterns(request):
    '''a function to retrieve patterns created by users the authenticated user is following'''
    user = request.user
    # check for auth
    if not user.is_authenticated:
        return JsonResponse({"error": "Authentication is required"}, status=401)
    
    # filter patterns based on the user's following
    following_users = Follow.objects.filter(follower=user).values_list('following', flat=True)
    patterns = Pattern.objects.filter(creator__in=following_users).order_by('-created_at')

    # serialize and return patterns
    serializer = PatternListSerializer(patterns, many=True)
    return JsonResponse({
        'data': serializer.data
    })

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([])
def get_explore_patterns(request):
    '''a function to fetch patterns created by other users the authenticated user does not follow'''
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({"error": "Authentication is required"}, status=401)
    
    # Filter patterns based on the following relationships
    following_users = Follow.objects.filter(follower=user).values_list('following', flat=True)
    
    # Exclude the patterns by the current user and the users that the user is following
    patterns = Pattern.objects.exclude(creator=user)  # Exclude patterns from the user
    patterns = patterns.exclude(creator__in=following_users)  # Exclude patterns from users that the current user is following
    patterns = patterns.order_by('-created_at')
    
    # serialize and return
    serializer = PatternListSerializer(patterns, many=True)
    return JsonResponse({
        'data': serializer.data
    })

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([])
def create_pattern(request, user_id):
    '''a function to create a pattern by the currently authenticated user'''
    user = request.user
    # check for auth
    if not user.is_authenticated:
        return JsonResponse({"error": "you must be authenticated to perform this"})
    
    # use pattern creation serializer to create an instance of a pattern
    serializer = PatternCreateSerializer(data=request.data)

    # if the serialized pattern is valid, save it to the database and reply success
    if serializer.is_valid():
        post = serializer.save()
        print(post)
        return JsonResponse({
            "message": "Pattern created successfully!",
        }, status=status.HTTP_201_CREATED)
    # otherwise reply with error
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([]) 
def get_patterns_with_search(request):
    '''a function to get patterns that match a search query provided by the request'''
    user = request.user 
    # check for authentication
    if not user.is_authenticated:
        return JsonResponse({"error": "you must be authenticated to perform this"})
    
    # extract the query from the search params
    search_query = request.GET.get('search_query', None)
    # start with all patterns
    patterns = Pattern.objects.all()
    # exclude user's own patterns
    patterns = patterns.exclude(creator=user)
    
    # if there is a search query, filter the patterns by name and description
    if search_query:
        patterns = patterns.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )

    # order by difficulty
    patterns = patterns.order_by('difficulty')
    # serialize and return
    serializer = PatternListSerializer(patterns, many=True)
    return JsonResponse({'data': serializer.data})

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def get_pattern_by_id(request, pattern_id):
    '''retrieve a pattern by its id to display all of its information'''
    # get the object by id, serialize and return
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
    '''a function to get a user's information by their id'''
    # retrieve the object, serialize and return
    user = get_object_or_404(User, id=user_id)
    serializer = UserSerializer(user)
    return JsonResponse({
        'data': serializer.data
    })

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def get_user_posts(request, user_id):
    '''a function to get a specific user's posts'''
    # filter by matching id with user_id, serialize and return
    posts = Post.objects.filter(user=user_id).order_by('-created_at')
    serializer = PostListSerializer(posts, many=True)
    return JsonResponse({
        'data': serializer.data
    })

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def get_user_patterns(request, user_id):
    '''a function to get all patterns created by a specific user'''
    # match the user_id parameter with creator of patterns
    patterns = Pattern.objects.filter(creator=user_id).order_by('-created_at')
    serializer = PatternListSerializer(patterns, many=True)
    return JsonResponse({
        'data': serializer.data
    })

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def get_user_followers(request, user_id):
    '''a function to retrieve all of a specific user's followers'''
    # filter the follow objects that FOLLOW the requested user
    follows = Follow.objects.filter(following=user_id)
    serializer = FollowerListSerializer(follows, many=True)
    return JsonResponse({
        'data': serializer.data
    })

#------FOLLOW VIEWS---------

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def get_user_following(request, user_id):
    '''a function to retrieve all of a specific user's following'''
    # filter the follow objects that the user FOLLOWS
    follows = Follow.objects.filter(follower=user_id)
    serializer = FollowingListSerializer(follows, many=True)
    return JsonResponse({
        'data': serializer.data
    })

@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([])
def update_user(request):
    '''a function to update the user's information (just avatar, link, and bio)'''
    user = request.user

    # check for authentication
    if not user.is_authenticated:
        return JsonResponse({"error": "you must be authenticated to perform this"})
    
    # retrieve the avatar file, link, and bio from the request (empty is okay)
    avatar = request.FILES.get('avatar')
    link = request.data.get('link')
    bio = request.data.get('bio')
    
    # Update the profile picture if it was provided, otherwise leave it as is
    if avatar:
        user.avatar = avatar   
    user.bio = bio
    user.link = link

    # save the user's information and return the details
    user.save()
    serializer = UserSerializer(user)
    return JsonResponse({'data': serializer.data})


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([])
def create_follow(request, other_id):
    '''a function to create a follow object between current authenticated user and 
    another user specified by the other_id'''
    user = request.user
    # check for authentication
    if not user.is_authenticated:
        return JsonResponse({"error": "You must be authenticated to perform this"}, status=status.HTTP_401_UNAUTHORIZED)
    
    # ensure the other user exists
    try:
        other_user = User.objects.get(id=other_id)
    except User.DoesNotExist:
        return JsonResponse({"error": "User to follow does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    # pass data to serializer which will populate the required fields
    data = {'following': other_id}
    serializer = FollowCreateSerializer(data=data, context={'request': request})
    
    # if the serializer is valid, save the follow and return a resopnse indicating success
    if serializer.is_valid():
        follow = serializer.save()  # Save the follow instance
        return JsonResponse({
            "message": "Successfully followed!",
            "follow_id": str(follow.id),  # Optionally return the follow ID
        }, status=status.HTTP_201_CREATED)
    # else return an error
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([]) 
def search_users(request):
    '''a function which allows the current user to search for other users in the database'''
    user = request.user 
    # ensure the user is authenticated
    if not user.is_authenticated:
        return JsonResponse({"error": "you must be authenticated to perform this"})
    # retrieve the search query from the request params, default to None if not found
    search_query = request.GET.get('search_query', None)
    # start with all patterns
    users = User.objects.all()
    # exclude self
    users = users.exclude(id=user.id)
    # if the search query exists, filter the users by if their username or name contains the query
    if search_query:
        users = users.filter(
            Q(name__icontains=search_query) | Q(username__icontains=search_query)
        )
    # serialize the users and return the list
    serializer = UserSerializer(users, many=True)
    return JsonResponse({'data': serializer.data})



#--------INVENTORY VIEWS-------
@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def get_inventory(request, user_id):
    '''a function to retrieve the inventory of a user'''
    # filter by the user_id parameter and order by the type of item and how recent it was
    items = InventoryItem.objects.filter(user=user_id).order_by('created_at', 'item_type')
    serializer = InventoryListSerializer(items, many=True)
    return JsonResponse({
        'data': serializer.data
    })

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([])
def create_inventory_item(request, user_id):
    '''a function to create an inventory item for the authenticated user'''
    user = request.user
    # check for authentication
    if not user.is_authenticated:
        return JsonResponse({"error": "you must be authenticated to perform this"})
    
    # use inventory creation serializer to validate data, and save if so
    serializer = InventoryCreateSerializer(data=request.data)
    if serializer.is_valid():
        post = serializer.save()
        print(post)
        return JsonResponse({
            "message": "Item created successfully!",
        }, status=status.HTTP_201_CREATED)
    # return error
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([])
def delete_inventory_item(request, inventory_id):
    ''' a function to delete a specified inventory item from the user's inventory'''
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({"error": "you must be authenticated to perform this"})
    # retrieve object and delete
    item = get_object_or_404(InventoryItem, id=inventory_id)
    item.delete()
    # return success message
    return JsonResponse({"message": "item successfully deleted"})