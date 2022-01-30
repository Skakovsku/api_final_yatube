from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet

app_name = 'api'

router = DefaultRouter()
router.register('posts', PostViewSet)

urlpatterns = [
    path(
        'v1/follow/',
        FollowViewSet.as_view(
            {'get': 'list',
             'post': 'create'}
        )
    ),
    path('v1/groups/<int:id>/', GroupViewSet.as_view({'get': 'retrieve'})),
    path('v1/groups/', GroupViewSet.as_view({'get': 'list'})),
    path(
        'v1/posts/<int:id>/comments/<int:pk>/',
        CommentViewSet.as_view(
            {'get': 'retrieve',
             'put': 'update',
             'patch': 'partial_update',
             'delete': 'destroy'}
        )
    ),
    path(
        'v1/posts/<int:pk>/comments/',
        CommentViewSet.as_view(
            {'get': 'list',
             'post': 'create'}
        )
    ),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
    path('v1/', include(router.urls)),
]
