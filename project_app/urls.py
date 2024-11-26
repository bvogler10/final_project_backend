from django.urls import path
from . import api

urlpatterns = [
    path('', api.post_list, name='api_post_list'),
]