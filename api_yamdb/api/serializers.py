from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from reviews.models import User, Title, Genre, Category, Review, Comment
from .validators import validate_username, char_validator


class UserSerializer(serializers.Serializer):
    """Сериализатор для создания пользователей"""
    username = serializers.CharField(
        max_length=150,
        validators=[validate_username, char_validator],
        required=True,
    )
    email = serializers.EmailField(
        max_length=254,
        required=True,
    )

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        user_data = User.objects.filter(username=username, email=email)
        if not user_data.exists():
            if User.objects.filter(username=username):
                raise ValidationError(
                    'Пользователь с таким username существует'
                )
            if User.objects.filter(email=email):
                raise ValidationError('Пользователь с таким email существует')
        return super().validate(attrs)


class GetJWTSerializer(serializers.Serializer):
    """Сериалайзер для получения JWT-токена"""
    username = serializers.CharField(
        max_length=150,
        validators=[validate_username, char_validator],
        required=True,
    )
    confirmation_code = serializers.CharField(required=True)


class AdminEditUserSerializer(serializers.ModelSerializer):
    """Сериализатор для редактирования пользователей админом."""

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class UserEditSerializer(serializers.ModelSerializer):
    """Сериалайзер для управления профилем пользователя."""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')
        read_only_fields = ('role',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(
        read_only=True, many=True
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )


class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True
    )

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    def validate(self, data):
        request = self.context.get('request')
        title = get_object_or_404(
            Title, pk=self.context.get('view').kwargs.get('title_id')
        )
        review = Review.objects.filter(title_id=title, author=request.user)
        if request.method == 'POST' and review.exists():
            raise ValidationError(
                'Можно оставить только один отзыв на произведение!'
            )
        return super().validate(data)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
