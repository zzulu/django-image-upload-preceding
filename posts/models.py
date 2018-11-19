from django.db import models
from django.urls import reverse

# Create your models here.
class Post(models.Model):
    image = models.ImageField()
    content = models.TextField()
    
    def get_absolute_url(self):
        return reverse('posts:detail', kwargs={'pk': self.pk})