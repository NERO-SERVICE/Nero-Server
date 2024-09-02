import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from news.models import NewsArticle

class Command(BaseCommand):
    help = 'Crawl ADHD news from Naver'

    def handle(self, *args, **kwargs):
        query = 'ADHD'
        url = f'https://search.naver.com/search.naver?where=news&query={query}'
        
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 뉴스 기사들을 가져오기
        news_items = soup.select('.news_tit')

        for item in news_items:
            title = item.get_text()
            link = item['href']

            # 이미 존재하는 뉴스 기사를 저장하지 않음
            if not NewsArticle.objects.filter(link=link).exists():
                NewsArticle.objects.create(title=title, link=link)
                self.stdout.write(self.style.SUCCESS(f'Saved: {title}'))

        self.stdout.write(self.style.SUCCESS('Crawling completed successfully'))
