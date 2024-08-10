from django.db import models
from django.conf import settings

class DrfProduct(models.Model):
    id = models.AutoField(primary_key=True) 
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    productPrice = models.IntegerField(default=0)
    isFree = models.BooleanField(default=False)
    imageUrls = models.JSONField(default=list)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    viewCount = models.IntegerField(default=0)
    status = models.CharField(max_length=50, choices=[
        ('sale', '판매중'),
        ('reservation', '예약중'),
        ('soldOut', '판매완료'),
        ('cancel', '취소')
    ])
    wantTradeLocation = models.JSONField(null=True, blank=True)
    wantTradeLocationLabel = models.CharField(max_length=255, null=True, blank=True)
    categoryType = models.CharField(max_length=255)
    likers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_products', blank=True)

    def __str__(self):
        return self.title