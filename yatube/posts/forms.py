from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group')
        labels = {
            'text': _('Текст'),
            'group': _('Группа'),
        }
        help_texts = {
            'text': _('Text for youtr post'),
            'group': _('Group to which this post belongs to'),
        }
