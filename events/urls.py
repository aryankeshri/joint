from django.conf.urls import url, include
from .views import *


urlpatterns = [
    url(r'^list/$', PostAPIViewSet.as_view({'get': 'list', }), name='post_list'),
    url(r'^create/$', PostAPIViewSet.as_view({'post': 'create', }), name='post_create'),
    url(r'details/$', PostAPIViewSet.as_view({'post': 'post_detail', }),
        name='post_detail'),
    url(r'^comment/create/$', CommentAPIViewSet.as_view({'post': 'create', }),
        name='comment_create'),
]