from django.db import models
from django.urls import reverse
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

def post_image_path(instance, filename):
    return 'posts/{}/{}'.format(instance.pk, filename)

# Create your models here.
class Post(models.Model):
    image = ProcessedImageField(
				upload_to=post_image_path,               # 저장 위치
                processors=[ResizeToFill(300, 300)],     # 처리할 작업 목록
                format='JPEG',                           # 저장 포맷
                options={'quality':90},                  # 옵션
            )
    content = models.TextField()
    
    def get_absolute_url(self):
        return reverse('posts:detail', kwargs={'pk': self.pk})