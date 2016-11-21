from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
# Create your models here.


class Image(models.Model):
    picture = models.ImageField('Изображение', upload_to='image_store/')
    description = models.CharField('Описание', max_length=250)
    key = models.SlugField(max_length=6, unique=True)
    view_count = models.PositiveIntegerField('Число просмотров', default=0)
    likes = models.PositiveIntegerField('Число лайков', default=0)
    upload_datetime = models.DateTimeField('Загружено', default=timezone.now)
    last_view_datetime = models.DateTimeField(
        'Просмотрено', blank=True, null=True)

    def __str__(self):
        return '{}-{} /{}/'.format(self.picture, self.key, self.description)

    def get_absolute_url(self):
        return reverse('pic_page', args=[self.key])