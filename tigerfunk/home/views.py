""" Views """
import datetime
from django.utils import timezone
from django.views import generic
from .models import Article

class HomeView(generic.ListView):
  """ Home view """
  model = Article
  template_name = 'home/index.html'
  context_object_name = 'articles'

class ArticleDetail(generic.DetailView):
  """ Single article view """
  model = Article
  template_name = 'home/detail.html'
  context_object_name = 'article'

class ArchivedArticle(generic.MonthArchiveView): # pylint: disable=too-many-ancestors
  """ Archived article view """
  queryset = Article.objects.filter(date__lt=timezone.now().date() - datetime.timedelta(days=30)) # pylint: disable=no-member
  date_field = 'date'
  template_name = 'home/archive.html'
  context_object_name = 'articles'
