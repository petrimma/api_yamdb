from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

v1_router = DefaultRouter()

v1_router.register('users', views.UserViewSet)
v1_router.register('genres', views.GenreViewSet, basename='genre')
v1_router.register('categories', views.CategoryViewSet, basename='category')
v1_router.register('titles', views.TitleViewSet, basename='title')
v1_router.register(r'titles/(?P<title_id>\d+)/reviews(/?P<review_id>\d+)?',
                   views.ReviewViewSet, basename='reviews')
v1_router.register((r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/'
                    r'comments(/?P<comment_id>\d+)?'),
                   views.CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/token/', views.GetJWTToken, name='token'),
    path('v1/auth/email/', views.email_confirmation, name='email'),
]
