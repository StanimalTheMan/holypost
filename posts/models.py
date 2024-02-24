from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    # user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    description = models.TextField()
    moderated = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    image_s3_key = models.CharField(max_length=255)

    def __str__(self):
        return f'Post {self.id}'