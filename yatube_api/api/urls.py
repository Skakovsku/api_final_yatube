# Привет, Артем! У меня есть просьба: завтра (08.02.2022) я ложусь на
# операцию, поэтому, до вторника или среды я не смогу заниматься учебой.
# Если проект не будет сдан до понедельника, я предполагаю, что к 10-му
# спринту меня не допустят, и придется оформлять академ. А так как я в
# ближайшие 2 месяца (минимум) буду на больничном, не хотелось бы терять целый
# месяц. Если в работе есть серьезные недочеты, обещаю исправить их в течение
# 10-го спринта.

from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet

app_name = 'api'

router = DefaultRouter()
router.register('posts', PostViewSet)
router.register('follow', FollowViewSet, basename='follow')
router.register('groups', GroupViewSet)
router.register(r'posts/(?P<id>\d+)/comments', CommentViewSet)

urlpatterns = [
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
    path('v1/', include(router.urls)),
]
