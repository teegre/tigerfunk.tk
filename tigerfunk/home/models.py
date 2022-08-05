""" Models """

import datetime
from random import randint
from django.db import models
from django.utils import timezone
from django.urls import reverse

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
  date = models.DateTimeField('date de publication')
  entry = models.TextField()
  tag = models.ManyToManyField(Tag)

  @property
  def is_new(self):
    """ Return True if article was published within current week """
    now = timezone.now().date()
    return self.date.date() > now - datetime.timedelta(days=7)

  @property
  def recently_published(self):
    """ Return True if article was published recently """
    now = timezone.now().date()
    recent = self.date.date() <= now - datetime.timedelta(days=0)
    return not self.is_archived and recent

  @property
  def is_archived(self):
    """ Return True if article was published more than 1 month ago """
    now = timezone.now().date()
    return self.date.date() < now - datetime.timedelta(days=30)

  class Meta: # pylint: disable=too-few-public-methods
    """ Ordering """
    ordering = ['-date']

  def get_absolute_url(self):
    return reverse('detail', args=[str(self.id)])

  def __str__(self):
    return f'{self.title}'

class PropagandaMessage(models.Model):
  """ Propaganda message """
  message = models.TextField(verbose_name='Message de propagande', max_length=255)

def get_random_message():
  """ Return a random propaganda message """
  max_id = PropagandaMessage.objects.all().aggregate(max_id=models.Max('id'))['max_id']
  while True:
    pk = randint(1, max_id)
    message = PropagandaMessage.objects.filter(pk=pk).first()
    if message:
      return message.message
