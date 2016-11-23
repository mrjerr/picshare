from django import forms
from .models import Image


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['picture', 'description']


class LoginForm(forms.Form):
    username = forms.CharField(label='User Name', max_length=64)
    password = forms.CharField(widget=forms.PasswordInput())
