from rest_framework import generics
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import NewsArticle
from .serializers import NewsArticleSerializer

class LatestNewsView(generics.ListAPIView):
    queryset = NewsArticle.objects.order_by('-created_at')[:4]
    serializer_class = NewsArticleSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class NewsPagination(PageNumberPagination):
    page_size = 20

class PaginatedNewsView(generics.ListAPIView):
    queryset = NewsArticle.objects.all().order_by('-created_at')
    serializer_class = NewsArticleSerializer
    pagination_class = NewsPagination
