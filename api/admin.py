from django.contrib import admin
from .models import User, Title, Category, Genre, Review, Comment


@admin.register(User)
class GroupAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'bio',
        'role',
    )
    search_fields = ('username', 'email')
    empty_value_display = '-пусто-'

