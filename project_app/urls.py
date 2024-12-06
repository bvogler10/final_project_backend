from django.urls import path
from . import api

from dj_rest_auth.jwt_auth import get_refresh_view
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView
from rest_framework_simplejwt.views import TokenVerifyView
from project_app.views.auth_views import CustomRegisterView

urlpatterns = [
    path('posts', api.get_all_posts, name='api_all_post_list'),
    path('user/<str:user_id>', api.get_user_by_id, name='api_user_info'),
    path('user_posts/<str:user_id>', api.get_user_posts, name='api_user_post_list'),
    path('update_user', api.update_user, name='update_user'),
    path('inventory/<str:user_id>', api.get_inventory, name='user_inventory'),
    path('posts/create_post', api.create_post, name='api_create_post'),
    path('auth/register/', CustomRegisterView.as_view(), name='rest_register'),
    path('auth/login/', LoginView.as_view(), name='rest_login'),
    path('auth/logout/', LogoutView.as_view(), name='rest_logout'),
    path('auth/token/refresh/', get_refresh_view().as_view(), name='token_refresh'),
]