from django.urls import path
from . import api

from dj_rest_auth.jwt_auth import get_refresh_view
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView
from rest_framework_simplejwt.views import TokenVerifyView
from project_app.views.auth_views import CustomRegisterView

urlpatterns = [
    path('posts', api.get_all_posts, name='api_all_post_list'),
    path('posts/create_post', api.create_post, name='api_create_post'),
    path('auth/register/', CustomRegisterView.as_view(), name='rest_register'),
    path('auth/login/', LoginView.as_view(), name='rest_login'),
    path('auth/logout/', LogoutView.as_view(), name='rest_logout'),
]