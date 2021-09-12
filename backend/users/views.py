from django.shortcuts import get_object_or_404

from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import Subscribe, User
from users.serializers import SubscribeSerializer, UserSerializer


class UserViewSet(UserViewSet):
    queryset = User.objects.all()
    pagination_class = LimitOffsetPagination

    @action(['get', ], detail=False)
    def me(self, request, *args, **kwargs):
        serializer = UserSerializer(
            self.request.user,
            context={'request': request}
        )
        return Response(serializer.data)

    @action(
        ['get', ],
        detail=False,
        url_path='subscriptions',
        url_name='subscriptions'
    )
    def subscriptions(self, request):
        paginator = LimitOffsetPagination()
        user = request.user
        ids = User.objects.values_list(
            'follower__author_id',
            flat=True).filter(id=user.id)
        queryset = User.objects.filter(id__in=ids)
        paginator_users = paginator.paginate_queryset(queryset, request)
        serializer = SubscribeSerializer(
            paginator_users,
            many=True,
            context={'request': request},
        )
        return paginator.get_paginated_response(serializer.data)


class SubscribeDetail(APIView):
    """
    Упраление подпиской
    """
    def get(self, request, pk):
        subscribe, created = Subscribe.objects.get_or_create(
            user=request.user,
            author_id=pk
        )
        if created:
            subscription = get_object_or_404(User, id=pk)
            serializer = SubscribeSerializer(
                subscription,
                context={'request': request}
            )
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            {'errors': 'Вы уже подписаны.'},
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, pk, format=None):
        subscribe = get_object_or_404(
            Subscribe,
            author_id=pk,
            user=request.user
        )
        subscribe.delete()
        return Response(
            {'detail': 'Вы отменили подписку.'},
            status=status.HTTP_204_NO_CONTENT
        )
