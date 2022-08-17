""" Custom tag """

from django import template
from django.utils import timezone

register = template.Library()

@register.simple_tag
def is_night():
  """
  Return True if current hour is less than 8
  and greater than 19.
  """
  return not timezone.localtime(timezone.now()).hour in range(8, 20)
