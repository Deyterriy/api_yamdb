from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'


class User(AbstractUser):
    """Кастомная модель пользователя"""

    ROLES = (
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin')
    )

    email = models.EmailField(max_length=254,
                              unique=True,
                              verbose_name='Почта')
    bio = models.TextField(blank=True, verbose_name='Биография')
    role = models.CharField(
        max_length=25,
        choices=ROLES,
        default=USER,
        verbose_name='Роль'
    )

    @property
    def is_admin(self):
        """Проверяем является ли пользователь админом или суперюзером"""
        return (
            self.role == ADMIN
            or self.is_superuser
            or self.is_staff
        )

    @property
    def is_moderator(self):
        """Проверяем является ли пользователь модератором"""
        return self.role == MODERATOR

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Category(models.Model):
    """Модель категорий"""
    name = models.CharField(max_length=256,
                            verbose_name='Наименование')
    slug = models.SlugField(max_length=50,
                            unique=True,
                            verbose_name='слаг')

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанров"""
    name = models.CharField(max_length=256,
                            verbose_name='Наименование')
    slug = models.SlugField(max_length=50,
                            unique=True,
                            verbose_name='слаг')

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведений"""
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
        related_name='title'
    )
    genre = models.ManyToManyField(
        Genre,
        through='TitleGenre',
        verbose_name='Жанр',
    )
    name = models.CharField(
        max_length=256, verbose_name='Наименование'
    )
    year = models.IntegerField(
        verbose_name='Год издания'
    )
    description = models.TextField(
        verbose_name='описание', blank=True
    )

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    """Модель для связи жанров и произведений"""

    title = models.ForeignKey(
        Title,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )
    genre = models.ForeignKey(
        Genre,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Жанр',
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель отзывов"""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Оценка'
    )
    text = models.TextField(
        verbose_name='Отзыв'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        unique_together = ('title', 'author',)

    def __str__(self):
        return f'{self.author} left review on {self.title}'


class Comment(models.Model):
    """Модель комментариев"""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    text = models.TextField(
        verbose_name='Комментарий'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Comment on {self.review} by {self.author}'
