from django.db import models
from django.conf import settings

class DrfProduct(models.Model):
    id = models.AutoField(primary_key=True) 
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    
    @property
    def imageUrls(self):
        # product와 연결된 ImageFile의 file.url 값을 리스트로 반환
        return [image.file.url for image in self.imageFiles.all()]

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-updatedAt'] 


class ImageFile(models.Model):
    product = models.ForeignKey(DrfProduct, related_name='imageFiles', on_delete=models.CASCADE)
    file = models.ImageField(upload_to='product_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.product.title}"