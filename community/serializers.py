from rest_framework import serializers
from .models import Post, Comment
from accounts.serializers import UserSerializer

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    
    class Meta:
        model = Comment
        fields = ['comment_id', 'user', 'content', 'created_at', 'updated_at', 'likes_count']
        read_only_fields = ['comment_id', 'user', 'created_at', 'updated_at', 'likes_count']

class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    thumbnail = serializers.ImageField(required=False, allow_null=True)
    
    class Meta:
        model = Post
        fields = ['post_id', 'user', 'content', 'thumbnail', 'created_at', 'updated_at', 'likes_count', 'comments_count', 'comments']
        read_only_fields = ['post_id', 'user', 'created_at', 'updated_at', 'likes_count', 'comments_count', 'comments']

class PostCreateSerializer(serializers.ModelSerializer):
    thumbnail = serializers.ImageField(required=False, allow_null=True, allow_empty_file=True)
    
    class Meta:
        model = Post
        fields = ['content', 'thumbnail']
        
class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content']