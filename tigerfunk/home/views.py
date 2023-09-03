""" Views """
import datetime
from django.utils import timezone
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

  # /!\ if rebuild db from scratch, comment the lines below:
  max_count = Tag.objects.all().aggregate(            # here
      count=Count(                                    # here
        'article', filter=Q(article__hidden=False)    # here
        )                                             # here
      )['count']                                      # here

  def tag_weight(self,pk):
    max_mg = 500
    art_count = Tag.objects.filter(pk=pk)[0].article_set.filter(hidden=False).count()
    return round(art_count*max_mg/self.max_count, 1);

  def custom_tag_query_set(self):
    data = Tag.objects.annotate(
      count=Count(
        'article', filter=Q(article__hidden=False)
      )
    ).filter(count__gt=0).values('id', 'name').order_by('-count', 'name')

    for tag in data:
      tag['weight'] = self.tag_weight(tag['id'])

    return data

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['articles'] = Article.objects.filter( # pylint: disable=no-member
      date__gte=timezone.now() - datetime.timedelta(days=30)
    )
    context['archives'] = Article.objects.filter( # pylint: disable=no-member
      date__lte=timezone.now() - datetime.timedelta(days=30), hidden=False
    )
   # pylint: disable=no-member
   # context['tags'] = Article.objects.filter(hidden=False).values(
   #     'tag__id', 'tag__name').annotate(count=Count(
   #       'tag__name')).order_by(
   #           '-count', 'tag__name')

    context['tags'] = self.custom_tag_query_set()

    context['message'] = get_random_message()

    return context

class ArticleDetail(generic.DetailView):
  """ Single article view """
  model = Article
  template_name = 'home/detail.html'
  context_object_name = 'article'

  slug_field = 'uid'
  slug_url_kwarg = 'uid'

class ArchivedArticle(generic.MonthArchiveView): # pylint: disable=too-many-ancestors
  """ Archived article view """
  queryset = Article.objects.filter(
    date__lt=timezone.now() - datetime.timedelta(days=30)).filter(
      hidden=False
    ) # pylint: disable=no-member
  date_field = 'date'
  template_name = 'home/archive.html'
  context_object_name = 'articles'

def articles_by_tag(request, name):
  """ Article list by tag """
  articles = Article.objects.filter(
    tag__name=name).filter(
      hidden=False)
  tag = Tag.objects.get(name=name)
  paginator = Paginator(articles, 15, orphans=2)

  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)

  return render(request, 'home/tag.html', {'tag': tag, 'page_obj': page_obj})

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
    return Article.objects.filter(hidden=False).order_by('-date')[:15] # pylint: disable=no-member

  def item_title(self, item):
    """Article title"""
    return item.title

  def item_pubdate(self, item):
    """Article published date"""
    return item.date

  def item_link(self, item):
    return reverse('detail', args=[item.uid])
