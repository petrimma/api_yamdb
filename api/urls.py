from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register('users', views.UserViewSet)


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/token/', views.GetJWTToken, name='token'),
    path('v1/auth/email/', views.email_confirmation, name='email'),
]
