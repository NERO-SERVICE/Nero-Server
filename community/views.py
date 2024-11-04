from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post, Comment
from .serializers import PostSerializer, PostCreateSerializer, CommentSerializer, CommentCreateSerializer
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10  # 기본 페이지 크기
    page_size_query_param = 'page_size'
    max_page_size = 200

# 메인 페이지: 게시물 리스트
class PostListView(generics.ListAPIView):
    queryset = Post.objects.filter(deleted_at__isnull=True).order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(content__icontains=search_query)
        return queryset

# 게시물 작성
class PostCreateView(generics.CreateAPIView):
    serializer_class = PostCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        post_serializer = PostSerializer(post, context={'request': request})
        response_data = post_serializer.data
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)


# 게시물 상세 조회, 수정, 삭제
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.filter(deleted_at__isnull=True)
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self):
        post = get_object_or_404(Post, post_id=self.kwargs['post_id'], deleted_at__isnull=True)
        return post

    def perform_update(self, serializer):
        post = self.get_object()
        if self.request.user != post.user:
            raise permissions.PermissionDenied("수정 권한이 없습니다.")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.user:
            raise permissions.PermissionDenied("삭제 권한이 없습니다.")
        instance.soft_delete()

# 댓글 작성
class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, post_id=post_id, deleted_at__isnull=True)
        serializer.save(user=self.request.user, post=post)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        comment_serializer = CommentSerializer(comment, context={'request': request})
        return Response(comment_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

# 댓글 리스트
class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post__post_id=post_id, deleted_at__isnull=True).order_by('-created_at')

# 댓글 상세 조회, 수정, 삭제
class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.filter(deleted_at__isnull=True)
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self):
        comment = get_object_or_404(Comment, comment_id=self.kwargs['comment_id'], deleted_at__isnull=True)
        return comment

    def perform_update(self, serializer):
        comment = self.get_object()
        if self.request.user != comment.user:
            raise permissions.PermissionDenied("수정 권한이 없습니다.")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.user:
            raise permissions.PermissionDenied("삭제 권한이 없습니다.")
        instance.soft_delete()

# 좋아요 기능
class LikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(Post, post_id=post_id, deleted_at__isnull=True)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            return Response({'message': '좋아요 취소'}, status=status.HTTP_200_OK)
        else:
            post.likes.add(request.user)
            return Response({'message': '좋아요'}, status=status.HTTP_200_OK)

class LikeCommentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, comment_id=comment_id, deleted_at__isnull=True)
        if request.user in comment.likes.all():
            comment.likes.remove(request.user)
            return Response({'message': '좋아요 취소'}, status=status.HTTP_200_OK)
        else:
            comment.likes.add(request.user)
            return Response({'message': '좋아요'}, status=status.HTTP_200_OK)