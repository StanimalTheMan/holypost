from django.db import models

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    moderated = models.BooleanField(defualt=False)