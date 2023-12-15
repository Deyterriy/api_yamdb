from django.contrib import admin

from .models import User, Genre, Title, Category, Review, Comment


class UserAdmin(admin.ModelAdmin):
    """Админка пользователей"""
    list_display = ('id', 'username', 'email', 'first_name', 'last_name',
                    'bio', 'role')
    search_fields = ('username',)
    list_filter = ('role',)
    empty_value_display = '-пусто-'


admin.site.register(User)
admin.site.register(Genre)
admin.site.register(Title)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Comment)
