""" Form """
from django import forms

class ContactForm(forms.Form):
  """ A contact form """
  sender = forms.EmailField(label='Votre e-mail')
  subject = forms.CharField(label='Objet', max_length=100)
  message = forms.CharField(widget=forms.Textarea)

