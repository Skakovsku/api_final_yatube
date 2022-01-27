from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import PostViewSet, UserViewSet

app_name = 'api'

router = DefaultRouter()
router.register('user', UserViewSet)
router.register('posts', PostViewSet)

urlpatterns = [
    path('v1/auth/', include('djoser.urls')),
    path('v1/auth/', include('djoser.urls.jwt')),
    # router is the last
    path('v1/', include(router.urls)),
]
