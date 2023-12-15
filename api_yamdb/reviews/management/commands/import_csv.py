from django.core.management.base import BaseCommand
from reviews.models import (
    Category, Genre, User, Title, Comment, Review, TitleGenre)
from csv import DictReader


class Command(BaseCommand):
    """Импорт категорий"""
    help = "Загружает данные из category.csv"

    def handle(self, *args, **options):
        for row in DictReader(
            open('./static/data/category.csv', encoding='utf-8')
        ):
            category = Category(
                id=row['id'], name=row['name'], slug=row['slug']
            )
            category.save()


class Command(BaseCommand):
    """Импорт жанров"""
    help = "Загружает данные genre.csv"

    def handle(self, *args, **options):
        for row in DictReader(
            open('./static/data/genre.csv', encoding='utf-8')
        ):
            genre = Genre(
                id=row['id'], name=row['name'], slug=row['slug']
            )
            genre.save()


class Command(BaseCommand):
    """Импорт пользователей"""
    help = "Загружает данные user.csv"

    def handle(self, *args, **options):
        for row in DictReader(
            open('./static/data/users.csv', encoding='utf-8')
        ):
            user = User(
                id=row['id'], username=row['username'], email=row['email'],
                first_name=row['first_name'], last_name=row['last_name'],
                bio=row['bio'], role=row['role']
            )
            user.save()


class Command(BaseCommand):
    """Импорт произведений"""
    help = "Загружает данные title.csv"

    def handle(self, *args, **options):
        for row in DictReader(
            open('./static/data/titles.csv', encoding='utf-8')
        ):
            category = Category.objects.get(id=row['category'])
            title = Title(
                id=row['id'], category=category,
                name=row['name'], year=row['year']
            )
            title.save()


class Command(BaseCommand):
    """Импорт связуещей таблицы произведений и жанров"""
    help = "Загружает данные из genre_title.csv"

    def handle(self, *args, **options):
        for row in DictReader(open('static/data/genre_title.csv',
                                   encoding="utf8")):
            genre_title = TitleGenre(
                id=row['id'],
                title=Title.objects.get(pk=row['title_id']),
                genre=Genre.objects.get(pk=row['genre_id'])
            )
            genre_title.save()


class Command(BaseCommand):
    """Импорт отзывов"""
    help = "Загружает данные из review.csv"

    def handle(self, *args, **options):
        for row in DictReader(
            open('./static/data/review.csv', encoding='utf-8')
        ):
            author = User.objects.get(id=row['author'])
            title = Title.objects.get(id=row['title_id'])
            review = Review(
                id=row['id'], title=title,
                text=row['text'], author=author,
                score=row['score'], pub_date=row['pub_date']
            )
            review.save()


class Command(BaseCommand):
    """Импорт комментариев"""
    help = "Загружает данные comment.csv"

    def handle(self, *args, **options):
        for row in DictReader(
            open('./static/data/comments.csv', encoding='utf-8')
        ):
            author = User.objects.get(id=row['author'])
            review = Review.objects.get(id=row['review_id'])
            comment = Comment(
                id=row['id'], review=review, author=author,
                text=row['text'], pub_date=row['pub_date']
            )
            comment.save()
