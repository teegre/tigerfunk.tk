""" Models """

import datetime
from django.db import models
from django.utils import timezone

class Tag(models.Model):
  """ A tag """
  name = models.CharField(max_length=15)

  class Meta: # pylint: disable=too-few-public-methods
    """ Ordering """
    ordering = ['name']

  def __str__(self):
    return f'{self.name}'

class Article(models.Model):
  """ An article """
  title = models.CharField(max_length=100)
  date = models.DateField('date de publication')
  entry = models.TextField()
  tag = models.ManyToManyField(Tag)

  @property
  def recently_published(self):
    """ Return True if article was published recently """
    now = timezone.now().date()
    recent = self.date <= now - datetime.timedelta(days=0)
    return not self.is_archived and recent

  @property
  def is_archived(self):
    """ Return True if article was published more than 1 month ago """
    now = timezone.now().date()
    return self.date < now - datetime.timedelta(days=30)

  class Meta: # pylint: disable=too-few-public-methods
    """ Ordering """
    ordering = ['-date']

  def __str__(self):
    return f'{self.title}'
