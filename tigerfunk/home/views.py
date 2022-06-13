""" Views """
# from django.shortcuts import render
from django.views import generic
from .models import ArticleModel

class HomeView(generic.ListView):
  """ Home view """
  model = ArticleModel
  template_name = 'home/index.html'
  context_object_name = 'articles'

class ArticleDetail(generic.DetailView):
  """ Single article view """
  model = ArticleModel
  template_name = 'home/detail.html'
  context_object_name = 'article'
