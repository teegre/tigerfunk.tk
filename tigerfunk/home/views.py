""" Views """
import datetime
from django.utils import timezone
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.shortcuts import render
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages
from django.db.models import Count
from .models import Tag, Article
from .forms import ContactForm

class HomeView(generic.ListView):
  """ Home view """
  model = Article
  template_name = 'home/index.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['articles'] = Article.objects.filter( # pylint: disable=no-member
      date__gte=timezone.now() - datetime.timedelta(days=30)
    )
    context['archives'] = Article.objects.filter( # pylint: disable=no-member
      date__lt=timezone.now() - datetime.timedelta(days=30)
    )
   # pylint: disable=no-member
    context['tags'] = Article.objects.values(
        'tag__id', 'tag__name').annotate(count=Count(
          'tag__name')).order_by(
              '-count', 'tag__name')

    return context

class ArticleDetail(generic.DetailView):
  """ Single article view """
  model = Article
  template_name = 'home/detail.html'
  context_object_name = 'article'

class ArchivedArticle(generic.MonthArchiveView): # pylint: disable=too-many-ancestors
  """ Archived article view """
  queryset = Article.objects.filter(date__lt=timezone.now() - datetime.timedelta(days=30)) # pylint: disable=no-member
  date_field = 'date'
  template_name = 'home/archive.html'
  context_object_name = 'articles'

class ArticleByTag(generic.DetailView):
  """ Article list by tag """
  model = Tag
  template_name = 'home/tag.html'

def contact_view(request):
  """ Send message from contact form """
  if request.method == 'POST':
    form = ContactForm(request.POST)
    if form.is_valid():
      subject = form.cleaned_data['subject']
      message = form.cleaned_data['message']
      sender = form.cleaned_data['sender']
      recipients = ['info@tigerfunk.tk']
      try:
        send_mail(subject, message, sender, recipients)
      except BadHeaderError:
        return HttpResponse('Ent??te invalide...')
      messages.success(request, 'Merci pour votre message !')
      return HttpResponseRedirect('/home/')
  else:
    form = ContactForm()

  return render(request, 'home/contact.html', {'form': form})

class LatestEntriesFeed(Feed):
  """RSS feed"""
  title = 'Tigerfunk.tk 500mg'
  link = ''
  description = 'Liste des derni??res publications.'

  def items(self):
    """An article entry"""
    return Article.objects.order_by('-date')[:15] # pylint: disable=no-member

  def item_title(self, item):
    """Article title"""
    return item.title

  def item_pubdate(self, item):
    """Article published date"""
    return item.date

  def item_link(self, item):
    return reverse('detail', args=[item.pk])
