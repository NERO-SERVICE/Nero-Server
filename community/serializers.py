from rest_framework import serializers
from .models import Post, PostImage, Comment
from accounts.serializers import UserSerializer

class PostImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = PostImage
        fields = ['image']

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    
    class Meta:
        model = Comment
        fields = ['comment_id', 'user', 'content', 'created_at', 'updated_at', 'likes_count']
        read_only_fields = ['comment_id', 'user', 'created_at', 'updated_at', 'likes_count']
        
class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content']
        
class PostSerializer(serializers.ModelSerializer):
    post_id = serializers.IntegerField(read_only=True)
    user = UserSerializer(read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    images = PostImageSerializer(many=True, read_only=True)
    isLiked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'post_id', 'user', 'content', 'created_at', 'updated_at',
            'likes_count', 'comments_count', 'comments', 'images', 'isLiked'
        ]
        read_only_fields = [
            'post_id', 'user', 'created_at', 'updated_at',
            'likes_count', 'comments_count', 'comments', 'images', 'isLiked'
        ]

    def get_isLiked(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            return obj.likes.filter(pk=request.user.pk).exists()
        return False


class PostCreateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(),
        required=False,
        allow_empty=True,
    )
    
    class Meta:
        model = Post
        fields = ['content', 'images']
        
    def create(self, validated_data):
        images = validated_data.pop('images', [])
        post = Post.objects.create(**validated_data)
        for image in images:
            PostImage.objects.create(post=post, image=image)
        return post