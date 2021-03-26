from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

v1_router = DefaultRouter()

v1_router.register('users', views.UserViewSet)
#v1_router.register(r"v1/titles/(?P<title_id>\d+)/reviews(/?P<review_id>\d+)?",
#                ReviewViewSet, basename="reviews")
#v1_router.register((r"v1/titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/"
#                 r"comments(/?P<comment_id>\d+)?"),
#                CommentViewSet, basename="comments")

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/token/', views.GetJWTToken, name='token'),
    path('v1/auth/email/', views.email_confirmation, name='email'),
]
