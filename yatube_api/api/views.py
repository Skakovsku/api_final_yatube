from django.core.exceptions import PermissionDenied

from posts.models import Comment, Follow, Group, Post
from rest_framework import permissions, status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if self.request.user != serializer.instance.author:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(PostViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if self.request.user != instance.author:
            raise PermissionDenied('Удаление чужого контента запрещено!')
        super(PostViewSet, self).perform_destroy(instance)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def retrieve(self, request, *args, **kwargs):
        if self.queryset.count() != 0:
            queryset = Group.objects.all()
            for group_id in queryset:
                if group_id.id == kwargs['id']:
                    serialiser = GroupSerializer(group_id)
                    return Response(serialiser.data)
        error = {"detail": "Страница не найдена."}
        return Response(error, status=status.HTTP_404_NOT_FOUND)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def list(self, request, *arg, **kwargs):
        if Post.objects.filter(pk=kwargs['pk']).count() == 0:
            error = {"detail": "Страница не найдена."}
            return Response(error, status=status.HTTP_404_NOT_FOUND)
        post = Post.objects.get(pk=kwargs['pk'])
        queryset = Comment.objects.filter(post=post)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        if Post.objects.filter(pk=kwargs['id']).count() != 0:
            post = Post.objects.get(pk=kwargs['id'])
            if Comment.objects.filter(post=post).count() != 0:
                queryset = Comment.objects.filter(post=post)
                for comment in queryset:
                    if comment.id == kwargs['pk']:
                        serialiser = CommentSerializer(comment)
                        return Response(serialiser.data)
        error = {"detail": "Страница не найдена."}
        return Response(error, status=status.HTTP_404_NOT_FOUND)

    def perform_create(self, serializer):
        post = Post.objects.get(pk=self.kwargs['pk'])
        serializer.save(
            author=self.request.user,
            post=post
        )

    def create(self, request, *args, **kwargs):
        if Post.objects.filter(pk=kwargs['pk']).count() == 0:
            error = {"detail": "Страница не найдена."}
            return Response(error, status=status.HTTP_404_NOT_FOUND)
        return super(CommentViewSet, self).create(request, *args, **kwargs)

    def perform_update(self, serializer):
        if self.request.user != serializer.instance.author:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(CommentViewSet, self).perform_update(serializer)

    def update(self, request, *args, **kwargs):
        print(args, kwargs)
        if Post.objects.filter(pk=kwargs['id']).count() == 0:
            error = {"detail": "Страница не найдена."}
            return Response(error, status=status.HTTP_404_NOT_FOUND)
        return super(CommentViewSet, self).update(request, *args, **kwargs)

    def perform_destroy(self, instance):
        if self.request.user != instance.author:
            raise PermissionDenied('Удаление чужого контента запрещено!')
        super(CommentViewSet, self).perform_destroy(instance)

    def destroy(self, request, *args, **kwargs):
        if Post.objects.filter(pk=kwargs['id']).count() == 0:
            error = {"detail": "Страница не найдена."}
            return Response(error, status=status.HTTP_404_NOT_FOUND)
        return super(CommentViewSet, self).destroy(request, *args, **kwargs)


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer

    def get_queryset(self):
        new_queryset = Follow.objects.filter(user=self.request.user)
        return new_queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
