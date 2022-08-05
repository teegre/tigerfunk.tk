""" Admin models """

from django.contrib import admin
from home.models import Tag, Article, PropagandaMessage

admin.site.register(Tag)
admin.site.register(Article)
admin.site.register(PropagandaMessage)
