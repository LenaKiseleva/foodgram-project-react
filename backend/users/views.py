from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from users.models import Subscribe, User
from users.serializers import (GetSubscribeSerializer, SubscribeSerializer,
                               UserSerializer)


@action(detail=False,
            methods=["GET"],
            url_path='subscriptions',
            url_name='subscriptions',
            permission_classes=[IsAuthenticated])
class UserViewSet(UserViewSet):
    # queryset = User.objects.all()
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset

    @action(["get",], detail=False)
    def me(self, request, *args, **kwargs):
        serializer = UserSerializer(self.request.user, context={'request': request})
        return Response(serializer.data)

    @action(["get",], detail=False)
    def subscriptions(self, request):
        paginator = LimitOffsetPagination()
        user = self.request.user
        ids = [_.author_id for _ in user.follower.all()]
        queryset = User.objects.filter(id__in=ids)
        paginator_users = paginator.paginate_queryset(queryset, request)
        serializer = SubscribeSerializer(paginator_users, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)


@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def subscribe(request, pk):
    if request.method == "GET":
        subscribe, created = Subscribe.objects.get_or_create(user=request.user, author_id=pk)
        if created:
            serializer = GetSubscribeSerializer(subscribe, context={'request': request})
            subscription = User.objects.get(id=pk)
            serializer_for_create = SubscribeSerializer(subscription, context={'request': request})
            return Response(serializer_for_create.data, status=status.HTTP_201_CREATED)
        return Response({'errors': 'Вы уже подписаны.'}, status=status.HTTP_201_CREATED)
    if request.method == "DELETE":
        subscribe = get_object_or_404(Subscribe, author_id=pk, user=request.user)
        subscribe.delete()
        return Response({'detail': 'Вы отменили подписку.'}, status=status.HTTP_204_NO_CONTENT)
    return Response({'detail': self.bad_request_message}, status=status.HTTP_400_BAD_REQUEST)
