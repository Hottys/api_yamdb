from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, jwt_token, user_register

v1_router = DefaultRouter()
v1_router.register(r'users', UserViewSet, basename='users')

auth_urlpatterns = [
    path('signup/', user_register, name='register'),
    path('token/', jwt_token, name='token')
]
v1_urlpatterns = [
    path('', include(v1_router.urls), name='v1_users'),
    path('auth/', include(auth_urlpatterns))
]
