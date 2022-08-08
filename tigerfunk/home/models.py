""" Models """

import datetime
import string
from random import randint, choice
from django.db import models
from django.db.models.signals import pre_save
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
  uid = models.CharField(max_length=12, blank=True)
  title = models.CharField(max_length=100)
  date = models.DateTimeField('date de publication')
  entry = models.TextField()
  hidden = models.BooleanField(default=False)
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
    return reverse('detail', kwargs={'uid': self.uid})

  def __str__(self):
    return f'{self.title}'

def uid_generator(size=12, chars=string.ascii_lowercase+string.digits):
  return ''.join(choice(chars) for _ in range(size))

def article_uid_generator(instance: Article):
  uid = uid_generator()
  article = instance.__class__
  if article.objects.filter(uid=uid).exists():
    return article_uid_generator(instance)
  return uid

def pre_save_create_article_uid(sender, instance, *arg, **kwargs):
  if not instance.uid:
    instance.uid = article_uid_generator(instance)

pre_save.connect(pre_save_create_article_uid, sender=Article)

class PropagandaMessage(models.Model):
  """ Propaganda message """
  message = models.TextField(verbose_name='Message de propagande', max_length=255)

def get_random_message():
  """ Return a random propaganda message """
  max_id = PropagandaMessage.objects.all().aggregate(max_id=models.Max('id'))['max_id']
  if not max_id:
    return '<b>tigerfunk.tk</b> vous souhaite la <b>bienvenue</b> !'
  while True:
    pk = randint(1, max_id)
    message = PropagandaMessage.objects.filter(pk=pk).first()
    if message:
      return message.message
