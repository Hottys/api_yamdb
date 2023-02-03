from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import CategoryViewSet, GenreViewSet, TitleViewSet

v1_router = DefaultRouter()
v1_router.register(r'titles', TitleViewSet)
v1_router.register(r'genres', GenreViewSet)
v1_router.register(r'categories', CategoryViewSet)
urlpatterns = [
    path('', include(v1_router.urls)),
]
