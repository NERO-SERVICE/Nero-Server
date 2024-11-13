from rest_framework import serializers
from .models import Post, PostImage, Comment, Report, CommentReport
from accounts.serializers import UserProfileSerializer

class PostImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = PostImage
        fields = ['image']

class CommentSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
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
    user = UserProfileSerializer(read_only=True)
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
    
    
class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'reporter', 'post', 'report_type', 'description', 'created_at']
        read_only_fields = ['id', 'reporter', 'created_at']

    def validate(self, data):
        if 'report_type' not in data:
            raise serializers.ValidationError("신고 유형을 선택해야 합니다.")
        return data
    
class CommentReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentReport
        fields = ['id', 'reporter', 'comment', 'report_type', 'description', 'created_at']
        read_only_fields = ['id', 'reporter', 'created_at']

    def validate(self, data):
        if 'report_type' not in data:
            raise serializers.ValidationError("신고 유형을 선택해야 합니다.")
        return data