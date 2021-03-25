from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import CommentViewSet, ReviewViewSet
from . import views

router = DefaultRouter()
router.register(r"v1/titles/(?P<title_id>\d+)/reviews(/?P<review_id>\d+)?",
                ReviewViewSet, basename="reviews")
router.register((r"v1/titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/"
                 r"comments(/?P<comment_id>\d+)?"),
                CommentViewSet, basename="comments")


urlpatterns = [
    path("", include(router.urls)),
path('v1/auth/token/', views.GetJWTToken.as_view, name='token'),
    path('v1/auth/email/', views.email_confirmation, name='email'),
]
