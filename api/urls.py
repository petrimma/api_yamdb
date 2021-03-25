from django.urls import path

from . import views


urlpatterns = [
    path('v1/auth/token/', views.GetJWTToken.as_view, name='token'),
    path('v1/auth/email/', views.email_confirmation, name='email'),
]