from django import forms
from froala_editor.widgets import FroalaEditor

from callback.models import Comment


class CommentCallbackForm(forms.ModelForm):
    text = forms.CharField(widget=FroalaEditor)

    class Meta:
        model = Comment
        fields = ('text', )
