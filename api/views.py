import string

from django.conf import settings
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer


@api_view(['POST'])
@permission_classes((AllowAny,))
def email_confirmation(request):
    if request.method == 'POST':
        user_email = request.data.get('email')

        if not user_email:
            return Response('E-mail не был передан.')

        confirmation_code = get_random_string(length=6,
                                              allowed_chars=string.digits)

        def random_username():
            email_username = user_email.split("@")[0]
            random_code = get_random_string(length=5,
                                            allowed_chars=string.digits)
            return f'{email_username}_{random_code}'

        def send_email():
            send_mail(
                subject='Yamdb Registration',
                message=f'Your confirmation code: {confirmation_code}',
                from_email=settings.EMAIL_FROM,
                recipient_list=[user_email, ],
                fail_silently=False
            )

        if User.objects.filter(email=user_email).exists():
            user = User.objects.get(email=user_email)
            serializer = UserSerializer(user, data=request.data,
                                        partial=True)
            if serializer.is_valid():
                serializer.save(confirmation_code=confirmation_code)
        else:
            User.objects.create_user(
                email=user_email,
                username=random_username(),
                confirmation_code=confirmation_code,
            )

        send_email()
        return Response('Код подтверждения был выслан на почту')


class GetJWTToken(viewsets.ModelViewSet):
    pass


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = AllowAny  # TODO Не забудь сменить
    filter_backends = [filters.SearchFilter]
    lookup_field = ['username', ]
    search_fields = ['username', ]
    pagination_class = PageNumberPagination
