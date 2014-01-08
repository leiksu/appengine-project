from django import forms
from django.forms import widgets

class BlogForm(forms.Form):
    blog_name = forms.CharField(label=u'Blog Name', max_length=100)
    blog_content = forms.CharField(label=u'Blog Content', widget=widgets.Textarea)