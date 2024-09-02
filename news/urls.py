from django.urls import path
from .views import LatestNewsView, PaginatedNewsView

app_name = "news"

urlpatterns = [
    path('latest/', LatestNewsView.as_view(), name='latest-news'),
    path('', PaginatedNewsView.as_view(), name='news-list'),
]