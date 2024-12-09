from django.urls import path
from . import api

from dj_rest_auth.jwt_auth import get_refresh_view
from dj_rest_auth.views import LoginView, LogoutView
from project_app.views.auth_views import CustomRegisterView

urlpatterns = [
    # post urls
    path('posts', api.get_all_posts, name='api_all_post_list'),
    path('posts/create_post', api.create_post, name='api_create_post'),
    path('posts/exclude_user', api.get_all_but_user_posts, name='api_exclude_user_posts'),
    path('posts/following', api.get_following_posts, name='api_user_following_posts'),
    path('posts/explore', api.get_explore_posts, name='api_user_explore_posts'),

    # pattern urls
    path('patterns/create_pattern/<str:user_id>', api.create_pattern, name='api_create_pattern'),
    path('patterns/', api.get_all_patterns, name='api_get_pattern'),
    path('pattern/<str:pattern_id>', api.get_pattern_by_id, name='api_pattern_info'),
    path('patterns/following', api.get_following_patterns, name='api_user_following_patterns'),
    path('patterns/explore', api.get_explore_patterns, name='api_user_explore_patterns'),
    path('patterns/exclude_user', api.get_all_but_user_patterns, name='api_exclude_user_patterns'),
    path('patterns/search_patterns/', api.get_patterns_with_search, name='api_get_patterns_with_search'),

    # user urls
    path('users/', api.search_users, name='api_search_user'),
    path('user/<str:user_id>', api.get_user_by_id, name='api_user_info'),
    path('user_posts/<str:user_id>', api.get_user_posts, name='api_user_post_list'),
    path('user_patterns/<str:user_id>', api.get_user_patterns, name='api_user_pattern_list'),
    path('update_user', api.update_user, name='update_user'),
    path('user/follow/<str:other_id>', api.create_follow, name='follow_user'),
    path('user/<str:user_id>/following', api.get_user_following, name='user_following'),
    path('user/<str:user_id>/followers', api.get_user_followers, name='user_followers'),

    # inventory urls
    path('inventory/<str:user_id>', api.get_inventory, name='user_inventory'),
    path('inventory/create_inventory/<str:user_id>', api.create_inventory_item, name='create_inventory_item'),
    path('inventory/delete_inventory/<str:inventory_id>', api.delete_inventory_item, name='delete_inventory_item'),

    # authentication urls
    path('auth/register/', CustomRegisterView.as_view(), name='rest_register'),
    path('auth/login/', LoginView.as_view(), name='rest_login'),
    path('auth/logout/', LogoutView.as_view(), name='rest_logout'),
    path('auth/token/refresh/', get_refresh_view().as_view(), name='token_refresh'),
]