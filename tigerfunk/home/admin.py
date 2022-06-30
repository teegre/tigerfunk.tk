""" Admin models """

from django.contrib import admin
from home.models import Tag, Article

admin.site.register(Tag)
admin.site.register(Article)
