from rest_framework import serializers
from .models import Post, Like
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    likes_count = serializers.IntegerField(read_only=True)
    # likes_user_id = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'author', 'created_at', 'updated_at', 'likes_count']

class IsStaffTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['is_staff'] = user.is_staff
        return token