import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from news.models import NewsArticle

class Command(BaseCommand):
    help = 'Crawl ADHD news from Naver'

    def handle(self, *args, **kwargs):
        query = 'ADHD'
        base_url = f'https://search.naver.com/search.naver?where=news&query={query}'
        headers = {'User-Agent': 'Mozilla/5.0'}

        news_count = 0
        max_news_count = 100
        page = 1

        while news_count < max_news_count:
            url = f'{base_url}&start={((page - 1) * 10) + 1}'
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')

            news_items = soup.select('.news_tit')

            if not news_items:
                break  # 더 이상 뉴스가 없으면 중단

            for item in news_items:
                if news_count >= max_news_count:
                    break

                title = item.get_text()
                link = item['href']

                if not NewsArticle.objects.filter(link=link).exists():
                    NewsArticle.objects.create(title=title, link=link)
                    news_count += 1
                    self.stdout.write(self.style.SUCCESS(f'Saved: {title}'))

            page += 1

        self.stdout.write(self.style.SUCCESS(f'Crawling completed successfully. {news_count} news articles were saved.'))
