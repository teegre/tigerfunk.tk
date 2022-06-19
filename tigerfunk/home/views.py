""" Views """
# from django.shortcuts import render
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
