from django import forms
from django.contrib.auth.models import User


class UploadFileForm(forms.Form):
    file  = forms.FileField()


class UserForm(forms.ModelForm):
    username=forms.CharField(help_text="Please enter a username.")
    email=forms.CharField(help_text="Please enter your email.")

    password=forms.CharField(widget=forms.PasswordInput(),help_text="Please enter a password.")

    class Meta:
        model = User
        fields = ('username','email','password')


