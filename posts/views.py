from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.decorators import action
from .serializers import PostSerializer
from .models import Post, Like
from .permissions import IsAuthorOrReadOnly
from django.db.models import Count
from rest_framework.throttling import UserRateThrottle
# Create your views here.

# class PostList(generics.ListCreateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    serializer_class = PostSerializer

    search_fields = ["title", "body"]
    ordering_fields = ["created_at", "updated_at", "id"]
    filterset_fields = ["author"]
    
    def get_queryset(self):
        return (
            Post.objects
                .select_related("author")
                .prefetch_related("post_likes")
                .order_by("-created_at")
                .annotate(likes_count=Count("post_likes", distinct=True))
        )
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, permission_classes=[IsAuthenticated], methods=["post"], throttle_classes=UserRateThrottle)
    def like(self, request, pk=None):
        post = self.get_object()
        Like.objects.get_or_create(user=request.user, post=post)
        return Response({"liked": True, "likes": post.post_likes.count()})
    
    @action(detail=True, permission_classes=[IsAuthenticated], methods=["delete"], throttle_classes=UserRateThrottle)
    def unlike(self, request, pk=None):
        post = self.get_object()
        # post.likes.remove(request.user)
        Like.objects.filter(user=request.user, post=self.get_object()).delete()
        return Response({"liked": True, "likes": post.post_likes.count()})