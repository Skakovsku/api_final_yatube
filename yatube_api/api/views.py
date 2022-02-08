from rest_framework import filters, status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from posts.models import Comment, Follow, Group, Post

from .permissions import GroupPermission, PostCommentPermission
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (PostCommentPermission,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (GroupPermission,)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (PostCommentPermission,)

    def list(self, request, *arg, **kwargs):
        if Post.objects.filter(pk=kwargs['id']).count() == 0:
            error = {"detail": "Страница не найдена."}
            return Response(error, status=status.HTTP_404_NOT_FOUND)
        post = Post.objects.get(pk=kwargs['id'])
        queryset = Comment.objects.filter(post=post)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        if Post.objects.filter(pk=kwargs['id']).count() != 0:
            post = Post.objects.get(pk=kwargs['id'])
            if Comment.objects.filter(post=post).count() != 0:
                queryset = Comment.objects.filter(post=post)
                for comment in queryset:
                    if str(comment.id) == kwargs['pk']:
                        serialiser = CommentSerializer(comment)
                        return Response(serialiser.data)
        error = {"detail": "Страница не найдена."}
        return Response(error, status=status.HTTP_404_NOT_FOUND)

    def perform_create(self, serializer):
        post = Post.objects.get(pk=self.kwargs['id'])
        serializer.save(
            author=self.request.user,
            post=post
        )

    def create(self, request, *args, **kwargs):
        if Post.objects.filter(pk=str(kwargs['id'])).count() == 0:
            error = {"detail": "Страница не найдена."}
            return Response(error, status=status.HTTP_404_NOT_FOUND)
        return super(CommentViewSet, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if Post.objects.filter(pk=kwargs['id']).count() == 0:
            error = {"detail": "Страница не найдена."}
            return Response(error, status=status.HTTP_404_NOT_FOUND)
        return super(CommentViewSet, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if Post.objects.filter(pk=kwargs['id']).count() == 0:
            error = {"detail": "Страница не найдена."}
            return Response(error, status=status.HTTP_404_NOT_FOUND)
        return super(CommentViewSet, self).destroy(request, *args, **kwargs)


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ['=following__username', ]

    def get_queryset(self):
        new_queryset = Follow.objects.filter(user=self.request.user)
        return new_queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
