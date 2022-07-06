"""home URL Configuration"""

from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
  path('', views.HomeView.as_view(), name='index'),
  path('<int:pk>/', views.ArticleDetail.as_view(), name='detail'),
  path('<int:year>/<int:month>/', views.ArchivedArticle.as_view(month_format='%m'), name='archive'),
  path('tag/<int:pk>/', views.ArticleByTag.as_view(), name='tag'),
  path('contact/', views.contact_view, name='contact'),
  path('feed/', views.LatestEntriesFeed(), name='feed'),
]
