from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title, User


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


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'year',
        'description',
        'category',
    )
    empty_value_display = '-пусто-'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Genre)
class GenreAmdin(admin.ModelAdmin):
    list_display = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'author',
        'score',
        'pub_date',
    )
    search_fields = ('score',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'review',
        'text',
        'author',
        'pub_date',
    )
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'
