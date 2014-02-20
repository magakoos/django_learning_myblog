#coding=utf8
from django.forms import ModelForm, Textarea

from apps.blogeg.models import Comment


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['email', 'content']
        widgets = {
            'content': Textarea(attrs={'cols': 26, 'rows': 10}),
        }
