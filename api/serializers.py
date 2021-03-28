from rest_framework import serializers
from rest_framework.validators import ValidationError

from .models import Comment, Review, User, Genre, Category, Title


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )
    review = serializers.ReadOnlyField(source="review.id")

    class Meta:
        fields = "__all__"
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )
    title = serializers.ReadOnlyField(source="title.id")

    class Meta:
        fields = "__all__"
        model = Review


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'bio',
            'email',
            'role',
        ]


class SendCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        normal_email = value.lower()
        if User.objects.filter(email=normal_email).exists():
            raise serializers.ValidationError("Not unique email.")
        return normal_email


class UserTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, write_only=True)
    confirmation_code = serializers.CharField(required=True, write_only=True)

    def validate_email(self, value):
        if not value:
            raise ValidationError('Email address is required.')
        return value.lower()

    def validate_confirmation_code(self, value):
        if not value:
            raise ValidationError('confirmation code is required.')
        return value


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        lookup_field = 'slug'
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        lookup_field = 'slug'
        model = Genre


class GenreField(serializers.SlugRelatedField):
    def to_internal_value(self, data):
        try:
            return self.get_queryset().get(**{self.slug_field: data})
        except (TypeError, ValueError):
            self.fail('invalid')

    def to_representation(self, value):
        return GenreSerializer(value).data


class CategoryField(serializers.SlugRelatedField):
    def to_internal_value(self, data):
        try:
            return self.get_queryset().get(**{self.slug_field: data})
        except (TypeError, ValueError):
            self.fail('invalid')

    def to_representation(self, value):
        return CategorySerializer(value).data


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    category = CategoryField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Title
