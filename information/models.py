from django.db import models
from django.conf import settings

class Information(models.Model):
    infoId = models.AutoField(primary_key=True)
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
        verbose_name = "개발자 공지"
        verbose_name_plural = "개발자 공지"


class InformationImageFile(models.Model):
    information = models.ForeignKey(Information, related_name='imageFiles', on_delete=models.CASCADE)
    file = models.ImageField(upload_to='info_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.information.title}"
