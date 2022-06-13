""" Models """

import datetime
from django.db import models
from django.utils import timezone

class ArticleModel(models.Model):
  """ Article Model """
  title = models.CharField(max_length=100)
  date = models.DateField('date de publication')
  entry = models.TextField()

  def recently_published(self):
    """ Return True if article was published recently """
    now = timezone.now().date()
    return self.date <= now - datetime.timedelta(days=0)


  class Meta:
    """ Order """
    ordering = [ '-date', ]

  def __str__(self):
    return f'{self.title}'
