from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import PostSerializer
from .models import Post
# Create your views here.

# class PostList(generics.ListCreateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
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
        )
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)