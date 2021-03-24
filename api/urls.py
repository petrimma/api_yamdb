from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import CommentViewSet, ReviewViewSet


router = DefaultRouter()
router.register(r"v1/titles/(?P<title_id>\d+)/reviews(/?P<review_id>\d+)?",
                ReviewViewSet, basename="reviews")
router.register((r"v1/titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/"
                 r"comments(/?P<comment_id>\d+)?"),
                CommentViewSet, basename="comments")


urlpatterns = [
    path("", include(router.urls)),
]
