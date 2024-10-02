from django.db import models
from django.conf import settings

class Notification(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def imageUrls(self):
        return [image.file.url for image in self.imageFiles.all()]

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-updated_at']
        verbose_name = "공지"
        verbose_name_plural = "공지"


class ImageFile(models.Model):
    notification = models.ForeignKey(Notification, related_name='imageFiles', on_delete=models.CASCADE)
    file = models.ImageField(upload_to='notification_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.notification.title}"
