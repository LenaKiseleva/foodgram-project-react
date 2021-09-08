from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet, subscribe

router = DefaultRouter()
router.register('users', UserViewSet, basename='User')

urlpatterns = [
    path('', include(router.urls)),
    path('users/<int:pk>/subscribe/', subscribe),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
