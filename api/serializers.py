from rest_framework import serializers

from .models import Comment, Review, User, Genre


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


class UserTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, write_only=True)
    confirmation_code = serializers.CharField(required=True, write_only=True)

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Genre