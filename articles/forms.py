from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'content')
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre nom'}),'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Votre email'}),'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Votre commentaire', 'rows': 5})}