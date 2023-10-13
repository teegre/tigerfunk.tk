""" Views """
import re
from datetime import timedelta
from collections import namedtuple
from django.utils.timezone import now
from django.views import generic
# from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.shortcuts import render
from django.core.paginator import Paginator
# from django.core.mail import send_mail, BadHeaderError
# from django.contrib import messages
from django.db.models import Count, Q
from .models import Tag, Article, get_random_message
# from .forms import ContactForm

class HomeView(generic.ListView):
  """ Home view """
  model = Article
  template_name = 'home/index.html'

  def tag_article_count(self):
    return Tag.objects.all().aggregate(
      count=Count(
        'article', filter=Q(article__hidden=False)
        )
      )['count']

  def tag_weight(self,pk):
    max_count = self.tag_article_count()
    max_mg = 500
    art_count = Tag.objects.filter(pk=pk)[0].article_set.filter(hidden=False).count()
    return round(art_count*max_mg/max_count, 1)

  def custom_tag_query_set(self):
    data = Tag.objects.annotate(
        count=Count(
          'article', filter=Q(article__hidden=False, article__date__lte=now())
      )
    ).filter(count__gt=0).values('id', 'name').order_by('-count', 'name')

    for tag in data:
      tag['weight'] = self.tag_weight(tag['id'])

    return data

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['articles'] = Article.objects.filter( # pylint: disable=no-member
      date__gte=now() - timedelta(days=30), hidden=False
    )
    context['archives'] = Article.objects.filter( # pylint: disable=no-member
      date__lte=now() - timedelta(days=30), hidden=False
    )
   # pylint: disable=no-member
   # context['tags'] = Article.objects.filter(hidden=False).values(
   #     'tag__id', 'tag__name').annotate(count=Count(
   #       'tag__name')).order_by(
   #           '-count', 'tag__name')

    context['tags'] = self.custom_tag_query_set()

    context['message'] = get_random_message()

    context['domain'] = self.request.build_absolute_uri('/')

    return context

class ArticleDetail(generic.DetailView):
  """ Single article view """
  model = Article
  template_name = 'home/detail.html'
  context_object_name = 'article'

  slug_field = 'uid'
  slug_url_kwarg = 'uid'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['domain'] = self.request.build_absolute_uri('/')
    context['current_url'] = self.request.build_absolute_uri()
    return context

class ArchivedArticle(generic.MonthArchiveView): # pylint: disable=too-many-ancestors
  """ Archived article view """
  date_field = 'date'
  template_name = 'home/archive.html'
  context_object_name = 'articles'
  queryset = Article.objects.all()

  def get_queryset(self):
    return self.queryset.filter(
    date__lt=now() - timedelta(days=30),
    hidden=False
  ) # pylint: disable=no-member

def all_articles(request):
  """ Show all articles """
  articles = Article.objects.filter(date__lte=now(), hidden=False).order_by('-date')
  paginator = Paginator(articles, 15, orphans=2)

  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)

  return render(
    request,
    'home/all.html',
    {'page_obj': page_obj, 'count': articles.count}
  )

def articles_by_tag(request, name):
  """ Article list by tag """
  articles = Article.objects.filter(
    tag__name=name).filter(
      date__lte=now(),
      hidden=False
    )
  tag = Tag.objects.get(name=name)
  paginator = Paginator(articles, 15, orphans=2)

  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)

  return render(
    request,
    'home/tag.html',
    {'tag': tag, 'page_obj': page_obj, 'count': articles.count}
  )

class SearchView(generic.ListView):
  model = Article
  template_name = 'home/search.html'

  def parse_search_date(self, date_scheme):
    ''' Parse a date YYYY/MM or YYYY/ '''
    date = date_scheme.split('/')
    Date = namedtuple('Date', ['year', 'month'])
    return Date(date[0], date[1])

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    articles = Article.objects.filter(date__lte=now(), hidden=False)

    wordlists = [ a.keywords.split() for a in articles if a.keywords ]
    wordlist = [word for words in wordlists for word in words]
    Word = namedtuple('Word', ['word', 'freq'])
    keywords = {Word(word, wordlist.count(word)) for word in wordlist}

    search_str = self.request.GET.get('q')
    if search_str:
      if re.match(r'^(19|20)\d{2}/(0[1-9]|1[0-2])?$', search_str):
        date = self.parse_search_date(search_str)
        if date.month:
          articles = articles.filter(date__year=date.year, date__month=date.month)
        else:
          articles = articles.filter(date__year=date.year)
      else:
        articles = articles.filter(
          Q(title__icontains=search_str) | Q(keywords__icontains=search_str),
        )

      context['articles'] = articles
      context['search_str'] = search_str

    context['keywords'] = keywords
    return context

# def contact_view(request):
#  """ Send message from contact form """
#  if request.method == 'POST':
#    form = ContactForm(request.POST)
#    if form.is_valid():
#      subject = form.cleaned_data['subject']
#      message = form.cleaned_data['message']
#      sender = form.cleaned_data['sender']
#      recipients = ['info@tigerfunk.tk']
#      try:
#        send_mail(subject, message, sender, recipients)
#      except BadHeaderError:
#        return HttpResponse('Entête invalide...')
#      messages.success(request, 'Merci pour votre message !')
#      return HttpResponseRedirect('/home/')
#  else:
#    form = ContactForm()
#
#  return render(request, 'home/contact.html', {'form': form})

class LatestEntriesFeed(Feed):
  """RSS feed"""
  title = 'tigerfunk.tk'
  link = ''
  description = 'Liste des dernières publications.'

  def items(self):
    """An article entry"""
    return Article.objects.filter(date__lte=now(), hidden=False).order_by('-date')[:15] # pylint: disable=no-member

  def item_title(self, item):
    """Article title"""
    return item.title

  def item_pubdate(self, item):
    """Article published date"""
    return item.date

  def item_link(self, item):
    return reverse('detail', args=[item.uid])
