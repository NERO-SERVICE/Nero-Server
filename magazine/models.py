from django.db import models
from django.conf import settings

class Magazine(models.Model):
    magazineId = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    @property
    def imageUrls(self):
        return [image.file.url for image in self.imageFiles.all()]

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-updatedAt']


class MagazineImageFile(models.Model):
    magazine = models.ForeignKey(Magazine, related_name='imageFiles', on_delete=models.CASCADE)
    file = models.ImageField(upload_to='magazine_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.magazine.title}"
