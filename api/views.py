import string

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from rest_framework import filters, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .models import User
from .serializers import (
    UserSerializer,
    UserTokenSerializer,
    SendCodeSerializer
)


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
