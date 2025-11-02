from django.shortcuts import render
from rest_framework import viewsets, serializers, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.decorators import action
from .serializers import PostSerializer
from .models import Post, Like
from .permissions import IsAuthorOrReadOnly
from django.db.models import Count
from rest_framework.throttling import UserRateThrottle
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse, inline_serializer, extend_schema_view
from drf_spectacular.types import OpenApiTypes
# Create your views here.

# class PostList(generics.ListCreateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

@extend_schema_view(
    list=extend_schema(tags=["Posts"]),
    retrieve=extend_schema(tags=["Posts"]),
    create=extend_schema(tags=["Posts"]),
    update=extend_schema(tags=["Posts"]),
    partial_update=extend_schema(tags=["Posts"]),
    destroy=extend_schema(tags=["Posts"]),
)
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

    @extend_schema(
        tags=["Likes"],
        operation_id="posts_like",
        request=None,
        responses={
            200: OpenApiResponse(
                description="Already liked",
                response=inline_serializer(
                name="LikeResponse",    
                fields={
                    "liked": serializers.BooleanField(),    
                    "created": serializers.BooleanField(),
                    "likes_count": serializers.IntegerField(),
                    },
                ),
                examples=[OpenApiExample("repeated", value={"liked": True, "created": False, "likes_count": 5})],
            ),
            201: OpenApiResponse(
                description="Created like",
                response=OpenApiTypes.OBJECT,
                examples=[OpenApiExample("first_like", value={"liked": True, "created": True, "likes_count": 6})],
            ),
            401: OpenApiResponse(description="Unauthorized",),
            429: OpenApiResponse(description="Too many requests",),
        },
    )
    @action(detail=True, permission_classes=[IsAuthenticated], methods=["post"], throttle_classes=[UserRateThrottle])
    def like(self, request, pk=None):
        post = self.get_object()
        _, created = Like.objects.get_or_create(user=request.user, post=post)
        return Response(
            {"liked": True, "created": created, "likes_count": post.post_likes.count()},
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
            )
    
    @extend_schema(
        tags=["Likes"],
        operation_id="posts_unlike",\
        request=None,
        responses={
            200: OpenApiResponse(
                description="Unliked",
                response=inline_serializer(
                name="UnlikeResponse",
                fields={
                    "liked": serializers.BooleanField(),
                    "likes_count": serializers.IntegerField(),
                    },
                ),
                examples=[OpenApiExample("ok", value={"liked": False, "likes_count": 5})],
            ),
            401: OpenApiResponse(description="Unauthorized",),
            429: OpenApiResponse(description="Too many requests",),
        }
    )
    @action(detail=True, permission_classes=[IsAuthenticated], methods=["delete"], throttle_classes=[UserRateThrottle])
    def unlike(self, request, pk=None):
        post = self.get_object()
        # post.likes.remove(request.user)
        Like.objects.filter(user=request.user, post=self.get_object()).delete()
        return Response({"liked": False, "likes_count": post.post_likes.count()}, status=status.HTTP_200_OK)