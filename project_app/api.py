from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .models import Post
from .serializers import PostListSerializer

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def post_list(request):
    posts = Post.objects.all()
    serializer = PostListSerializer(posts, many=True)
    return JsonResponse({
        'data': serializer.data
    })