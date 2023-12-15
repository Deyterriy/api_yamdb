from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (UserGetJWTToken, UserViewSet, UserCreateViewSet,
                    TitleViewSet, CategoryViewSet, GenreViewSet, ReviewViewSet,
                    CommentViewSet)

app_name = 'api'

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('titles', TitleViewSet)
router.register('genres', GenreViewSet)
router.register('categories', CategoryViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', UserCreateViewSet.as_view(), name='register'),
    path('v1/auth/token/', UserGetJWTToken.as_view(), name='token')
]
