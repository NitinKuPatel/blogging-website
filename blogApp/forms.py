from django import forms
from .models import Post
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = "__all__"
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'publish': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class CustomUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username','first_name','last_name','email','address','contact']

class EmailSendForm(forms.Form):
    name=forms.CharField()
    email=forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)
    