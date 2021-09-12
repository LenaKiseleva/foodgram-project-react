from django.urls import include, path

from rest_framework.routers import DefaultRouter

from users.views import SubscribeDetail, UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='User')

urlpatterns = [
    path('', include(router.urls)),
    path('users/<int:pk>/subscribe/', SubscribeDetail.as_view()),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
