from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import IsAuthenticated
from .mixins import MixinViewSet

from reviews.models import User, Title, Category, Genre, Review
from .serializers import (AdminEditUserSerializer, GetJWTSerializer,
                          UserSerializer, TitleSerializer,
                          CategorySerializer, GenreSerializer,
                          ReviewSerializer, CommentSerializer,
                          UserEditSerializer, TitleCreateSerializer)
from .permissions import (IsAdmin, IsAdminOrReadOnly,
                          IsAuthorModeratorAdminOrReadOnly)
from .filters import TitleFilter


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для управления пользователями."""
    queryset = User.objects.all()
    serializer_class = AdminEditUserSerializer
    lookup_field = 'username'
    filter_backends = [SearchFilter]
    search_fields = ['username']
    permission_classes = (IsAdmin,)
    http_method_names = ('get', 'post', 'delete', 'patch')

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=(IsAuthenticated,), url_path='me', )
    def me(self, request):
        serializer = UserEditSerializer(
            request.user, partial=True, data=request.data
        )
        if serializer.is_valid(raise_exception=True):
            if request.method == 'PATCH':
                serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class UserCreateViewSet(APIView):
    """Вьюсет для создания пользователя и отправки кода."""

    @staticmethod
    def send_code(email, confirmation_code):
        send_mail(
            subject='Код подтверждения',
            message=f'Код подтверждения: {confirmation_code}',
            from_email=settings.EMAIL_TEST,
            recipient_list=[email],
            fail_silently=True,
        )

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, _ = User.objects.get_or_create(**serializer.validated_data)
        confirmation_code = default_token_generator.make_token(user=user)
        self.send_code(user.email, confirmation_code)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserGetJWTToken(APIView):
    def post(self, request):
        serializer = GetJWTSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username, confirmation_code = serializer.validated_data.values()
        user = get_object_or_404(User, username=username)

        if not default_token_generator.check_token(user, confirmation_code):
            return Response(
                {'confirmation_code': 'Неверный код подтверждения'},
                status=status.HTTP_400_BAD_REQUEST
            )
        token = AccessToken.for_user(user)
        return Response(
            {'token': str(token)},
            status=status.HTTP_200_OK
        )


class CategoryViewSet(MixinViewSet):
    """Вьюсет категорий"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(MixinViewSet):
    """Вьюсет жанров"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleSerializer
        return TitleCreateSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет отзывов"""
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.select_related('author')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет комментариев"""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)

    def get_review(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(Review, title__id=title_id, id=review_id)

    def get_queryset(self):
        return self.get_review().comments.select_related('author')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())
