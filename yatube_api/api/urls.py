from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import PostViewSet, UserViewSet, GroupViewSet

app_name = 'api'

router = DefaultRouter()
router.register('user', UserViewSet)
router.register('posts', PostViewSet)

urlpatterns = [
    path('v1/groups/<int:id>/', GroupViewSet.as_view({'get': 'list'})),
    path('v1/groups/', GroupViewSet.as_view({'get': 'list'})),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
    # router is the last
    path('v1/', include(router.urls)),
]
