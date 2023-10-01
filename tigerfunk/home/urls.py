"""home URL Configuration"""

from django.urls import path
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from django.views.generic.base import TemplateView
from home.models import Article

from . import views


info_dict = {
  'queryset': Article.objects.filter(hidden=False),
  'date_field': 'date',
}

urlpatterns = [
  path('', views.HomeView.as_view(), name='index'),
  path('article/<slug:uid>/', views.ArticleDetail.as_view(), name='detail'),
  path(
    'archive/<int:year>/<int:month>/',
    views.ArchivedArticle.as_view(month_format='%m'),
    name='archive'
  ),
  path('tag/<slug:name>/', views.articles_by_tag, name='tag'),
  # path('contact/', views.contact_view, name='contact'),
  path('articles', views.all_articles, name='all'),
  path('feed/', views.LatestEntriesFeed(), name='feed'),
  path('sitemap/', sitemap,
    {'sitemaps': {'blog': GenericSitemap(info_dict, priority=0.6)}},
    name='django.contrib.sitemaps.views.sitemap'),
  path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='plain/text')),
]
