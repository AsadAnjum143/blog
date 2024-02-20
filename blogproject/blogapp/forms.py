from django import forms
from .models import CommentTable
class EmailSendForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    to = forms.CharField()
    comments = forms.CharField(widget= forms.Textarea, required=False)
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentTable
        fields = ('name','email','body')
    