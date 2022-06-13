"""home URL Configuration"""

from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
  path('', views.HomeView.as_view(), name='index'),
  path('<int:pk>/', views.ArticleDetail.as_view(), name='detail')
]
