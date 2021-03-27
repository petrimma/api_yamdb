import string

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from rest_framework import filters, status, viewsets, mixins
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .models import Review, Title, User, Genre
from .serializers import (
    UserSerializer,
    UserTokenSerializer,
    SendCodeSerializer,
    CommentSerializer,
    ReviewSerializer,
    GenreSerializer,
)
from .permissions import ReadOnly, IsAdmin, IsModerator, IsAuthor


@api_view(['POST'])
@permission_classes((AllowAny,))
def email_confirmation(request):
    def _random_username():
        symbols_gen = string.ascii_uppercase
        random_code = get_random_string(length=5,
                                        allowed_chars=symbols_gen)
        return f'USER_{random_code}'

    def _send_email():
        send_mail(
            subject='Yamdb Registration',
            message=f'Your confirmation code: {confirmation_code}',
            from_email=settings.EMAIL_FROM,
            recipient_list=[user_email, ],
            fail_silently=False
        )

    serializer = SendCodeSerializer(data=request.data)
    if serializer.is_valid():
        user_email = request.data.get('email')
        confirmation_code = get_random_string(length=8,
                                              allowed_chars=string.digits)

        if not User.objects.filter(email=user_email).exists():
            User.objects.create_user(
                email=user_email,
                username=_random_username(),
                confirmation_code=confirmation_code
            )

        _send_email()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((AllowAny,))
def GetJWTToken(request):
    serializer = UserTokenSerializer(data=request.data)
    if serializer.is_valid():
        email = request.data.get('email')
        confirmation_code = request.data.get('confirmation_code')
        user = get_object_or_404(User, email=email)
        if user.confirmation_code == confirmation_code:
            token = AccessToken.for_user(user)
            return Response({'token': str(token)}, status=status.HTTP_200_OK)
        return Response('confirmation code: неверный код',
                        status=status.HTTP_200_OK)

    return Response('Необходимо передать email и confirmation code.')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny, ]  # TODO Не забудь сменить
    filter_backends = [filters.SearchFilter]
    lookup_field = 'username'
    search_fields = ['username', ]
    pagination_class = PageNumberPagination
    
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination
    permission_classes = ReadOnly, IsAuthenticated, IsAuthor, IsModerator

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return review.comments.all()


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    permission_classes = ReadOnly, IsAuthenticated, IsAuthor, IsModerator

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return title.reviews.all()


class GenreViewSet(mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    #permission_classes = ReadOnly
    filter_backends = [filters.SearchFilter]
    search_fields = ('name', 'slug')
    lookup_field = 'slug'