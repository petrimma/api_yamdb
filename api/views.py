import string

from django.db.models import Avg
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets, mixins
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .filters import TitlesFilter
from .models import Review, Title, User, Genre, Category
from .permissions import (
    ReadOnly,
    IsModerator,
    IsAuthor,
    IsAdmin
)
from .serializers import (
    UserSerializer,
    UserTokenSerializer,
    SendCodeSerializer,
    CommentSerializer,
    ReviewSerializer,
    GenreSerializer,
    CategorySerializer,
    TitleSerializer,
    TitleRatingSerializer,
)


class ListPostDelete(mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     viewsets.GenericViewSet):
    """
    The class provides List, Post and Delete actions.
    """
    pass


@api_view(['POST'])
@permission_classes((AllowAny,))
def email_confirmation(request):
    """
    The class provides access to register users and send a confirmation code.
    """

    def _random_username():
        """Generates a random username """
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
    """
    - Getting JWT if confirmation_code is valid.
    - The confirmation code can be used only once,
      after which it becomes invalid.
    """
    serializer = UserTokenSerializer(data=request.data)
    if serializer.is_valid():
        email = request.data.get('email')
        confirmation_code = request.data.get('confirmation_code')
        user = get_object_or_404(User, email=email)

        if (user.confirmation_code == confirmation_code and
                not user.is_code_expired):
            token = AccessToken.for_user(user)
            user.is_code_expired = True
            user.save()

            return Response({'token': str(token)}, status=status.HTTP_200_OK)
        return Response('confirmation code или email не действительный',
                        status=status.HTTP_200_OK)

    return Response('Необходимо передать email и confirmation code.')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin, ]
    filter_backends = [filters.SearchFilter]
    lookup_field = 'username'
    search_fields = ['username', ]
    pagination_class = PageNumberPagination

    @action(methods=('GET', 'PATCH'),
            permission_classes=(IsAuthenticated,),
            detail=False)
    # api to /users/me/
    def me(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
        if request.method == 'PATCH':
            user = get_object_or_404(User, username=request.user.username)
            serializer = UserSerializer(user, request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return review.comments.all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [ReadOnly]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthor | IsModerator & IsAdmin]
        return [permission() for permission in permission_classes]


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return title.reviews.all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [ReadOnly]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthor | IsModerator & IsAdmin]
        return [permission() for permission in permission_classes]



class GenreViewSet(ListPostDelete):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [ReadOnly | IsAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ('name', 'slug')
    lookup_field = 'slug'
    pagination_class = PageNumberPagination


class CategoryViewSet(ListPostDelete):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [ReadOnly | IsAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ('name', 'slug')
    lookup_field = 'slug'
    pagination_class = PageNumberPagination


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    permission_classes = [ReadOnly | IsAdmin]
    filterset_class = TitlesFilter
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleRatingSerializer
        else:
            return TitleSerializer
