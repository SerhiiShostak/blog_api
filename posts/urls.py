from django.urls import path, include
from posts import views
from rest_framework.routers import DefaultRouter

app_name = 'posts'

router = DefaultRouter()
router.register('posts', views.PostViewSet, basename='posts')

urlpatterns = [
    path("", include(router.urls)),
]